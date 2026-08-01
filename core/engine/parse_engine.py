from __future__ import annotations

from core.connection import SubBus, Connection, ChipConnection
from core.pin import Pin
from core.utils import is_integer

class ParseEngine:
    def __init__(self, hdl: str) -> None:
        self.hdl = hdl
        self.index = 0
        self.chip_name = ""
        self.input_pins:  list[Pin]      = []
        self.output_pins: list[Pin]      = []
        self.chip_parts:   list[str]      = []
        self.chip_connections: list[ChipConnection] = []

    def parse(self) -> None:
        self.advance()
        self.parse_declaration()

    def advance(self) -> int:
        while self.index < len(self.hdl):
            if self.hdl[self.index] == " ":
                self.index += 1
            elif self.hdl[self.index] == "\n":
                self.index += 1
            elif self.hdl[self.index] == "/":
                self.consume_comment()
            else:
                break
        return self.index

    def peek(self) -> str:
        self.advance()
        return self.hdl[self.index] if self.index < len(self.hdl) else ""

    def consume_comment_to_end_line(self) -> int:
        if self.hdl.find("//", self.index) != self.index:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected comment starting with '//'")
        tmp = self.hdl.find("\n", self.index + 2)
        if tmp == -1:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected comment to end with 'newline'")
        self.index = tmp + 1
        return self.index

    def consume_comment_until_close(self) -> int:
        if self.hdl.find("/*", self.index) != self.index:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected comment starting with '/*'")
        tmp = self.hdl.find("*/", self.index + 2)
        if tmp == -1:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected comment to end with '*/'")
        self.index = tmp + 2
        return self.index

    def consume_comment(self) -> int:
        if self.hdl[self.index] != "/" or self.index + 1 > len(self.hdl):
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected comment")

        if self.hdl[self.index + 1] == "/":
            self.consume_comment_to_end_line()

        if self.hdl[self.index + 1] == "*":
            self.consume_comment_until_close()

        return self.index

    def consume_token(self) -> str:
        self.advance()
        old = self.index
        if self.index < len(self.hdl) and self.hdl[self.index].isalpha():
            self.index += 1
            while self.index < len(self.hdl) and self.hdl[self.index].isalnum():
                self.index += 1
        token = self.hdl[old: self.index]
        return token

    def consume_symbol(self) -> str:
        self.advance()
        old = self.index
        if self.index < len(self.hdl) and (not self.hdl[self.index].isalnum() and not self.hdl[self.index] in [" ", "\n"]):
            self.index += 1
        symbol = self.hdl[old: self.index]
        return symbol

    def consume_pin_name(self) -> str:
        token = self.consume_token()
        if len(token) == 0:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected pin name")
        return token

    def consume_chip_name(self) -> str:
        token = self.consume_token()
        if len(token) == 0:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected GateClass name")
        return token

    def consume_expected_token(self, expected_token: str) -> int:
        token = self.consume_token()
        if token != expected_token:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Missing '{expected_token}' keyword")
        return self.index

    def consume_expected_symbol(self, expected_symbol: str) -> int:
        self.advance()
        symbol = self.consume_symbol()
        if symbol != expected_symbol:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Missing '{expected_symbol}'")
        return self.index

    def parse_declaration(self) -> int:
        # consume 'CHIP' keyword
        self.consume_expected_token("CHIP")

        # consume chip name
        chip_name = self.consume_token()
        if len(chip_name) == 0:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Missing chip name")

        # consume '{' symbol
        self.consume_expected_symbol("{")

        # parse chip program
        self.parse_program()

        # consume '}' symbol
        self.consume_expected_symbol("}")

        return self.index

    def parse_program(self) -> int:
        # parse chip interface
        self.parse_interface()

        # parse chip implementation
        self.parse_implementation()
        return self.index

    def parse_interface(self) -> int:
        # parse input pins
        self.parse_input_interface()

        # parse output pins
        self.parse_output_interface()
        return self.index

    def parse_input_interface(self) -> int:
        self.consume_expected_token("IN")
        self.input_pins = self.parse_interface_pins()
        return self.index

    def parse_output_interface(self) -> int:
        self.consume_expected_token("OUT")
        self.output_pins = self.parse_interface_pins()
        return self.index

    def parse_interface_pins(self) -> list[Pin]:
        pins: list[Pin] = []
        while self.peek() != ";":
            # parse & save pin name
            pin = self.parse_interface_pin_token()
            pins.append(pin)

            if self.peek() == ";":
                break

            # parse ',' symbol
            self.consume_expected_symbol(",")

        # parse ';' symbol
        self.consume_expected_symbol(";")
        return pins

    def parse_interface_pin_token(self) -> Pin:
        # parse pin name
        pin_name = self.consume_pin_name()

        # check if pin is multi-bit
        if self.peek() != "[":
            return Pin(pin_name, 1)

        # consume '[' symbol
        self.consume_expected_symbol("[")

        # consume pin width
        old = self.index
        while self.index < len(self.hdl) and self.hdl[self.index] not in ["]", "\n"]:
            self.index += 1
        width = self.hdl[old: self.index]

        if self.peek() != "]":
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Pin '{pin_name}' missing ']'")

        # consume ']' symbol
        self.consume_expected_symbol("]")

        # check if pin width is numeric
        if not is_integer(width):
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: {pin_name}[{width}] has invalid bus width")
        if int(width) <= 0:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: {pin_name}[{width}] negative bus widths are not allowed")

        return Pin(pin_name, int(width))

    def parse_implementation(self) -> int:
        self.consume_expected_token("PARTS")

        self.consume_expected_symbol(":")

        while self.peek() != "}":
            self.parse_chip_part()

        return self.index

    def parse_chip_part(self) -> int:
        chip_name = self.consume_chip_name()
        self.chip_parts.append(chip_name)

        self.consume_expected_symbol("(")

        while self.peek() != ")":
            connection = self.parse_connection()
            self.chip_connections.append(ChipConnection(chip_name, connection))

            if self.peek() == ")":
                break

            self.consume_expected_symbol(",")

        self.consume_expected_symbol(")")

        self.consume_expected_symbol(";")

        return self.index

    def parse_connection(self) -> Connection:
        left = self.parse_implementation_pin_token(False)

        self.consume_expected_symbol("=")

        right = self.parse_implementation_pin_token(True)

        return Connection(left, right)

    def parse_implementation_pin_token(self, is_right: bool) -> SubBus:
        # consume pin name
        pin_name = self.consume_pin_name()

        # check if pin is right
        if is_right and pin_name in ["true", "false"]:
            return SubBus(pin_name, (0, -1))

        if self.peek() != "[":
            return SubBus(pin_name, (0, -1))

        # consume '[' symbol
        self.consume_expected_symbol("[")

        # consume bus pins
        old = self.index
        while self.index < len(self.hdl) and self.hdl[self.index] not in ["]", "\n"]:
            self.index += 1
        sub_bus = self.hdl[old: self.index]

        if self.peek() != "]":
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Pin '{pin_name}' missing ']'")

        # consume ']' symbol
        self.consume_expected_symbol("]")

        # check sub bus specification
        sub_bus_parts = sub_bus.split("..")

        if len(sub_bus_parts) == 1 and is_integer(sub_bus_parts[0]):
            width = int(sub_bus_parts[0])
            if width < 0:
                raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: {pin_name}[{sub_bus}] negative bit numbers are illegal")
            return SubBus(pin_name, (width, width))

        if len(sub_bus_parts) == 2 and is_integer(sub_bus_parts[0]) and is_integer(sub_bus_parts[1]):
            if int(sub_bus_parts[0]) < 0 or int(sub_bus_parts[1]) < 0:
                raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: {pin_name}[{sub_bus}] negative bit numbers are illegal")
            if int(sub_bus_parts[0]) > int(sub_bus_parts[1]):
                raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: {pin_name}[{sub_bus}] left bit number should be lower or equal to the right bit number")
            return SubBus(pin_name, (int(sub_bus_parts[0]), int(sub_bus_parts[1])))

        raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: {pin_name}[{sub_bus}] has an invalid sub bus specification")
