from __future__ import annotations
from core.pin import Pin

class Engine:
    def __init__(self, hdl: str) -> None:
        self.hdl = hdl

        self.index = 0

        self.chip_name = ""
        self.input_pins: list[Pin] = []
        self.output_pins: list[Pin] = []

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
        if self.index + 1 >= len(self.hdl) or self.hdl[self.index] != "/":
            raise Exception()

        if self.hdl[self.index + 1] == "/":
            self.consume_comment_to_end_line()

        if self.hdl[self.index + 1] == "*":
            self.consume_comment_until_close()

        return self.index

    def consume_alphanum(self):
        while self.index < len(self.hdl) and self.hdl[self.index].isalnum():
            self.index += 1
        return self.index

    def consume_token(self) -> str:
        old = self.index
        if self.index < len(self.hdl) and self.hdl[self.index].isalpha():
            self.index += 1
            while self.index < len(self.hdl) and self.hdl[self.index].isalnum():
                self.index += 1
        return self.hdl[old: self.index]

    def consume_symbol(self) -> str:
        old = self.index
        if self.index < len(self.hdl) and (not self.hdl[self.index].isalnum() and not self.hdl[self.index] in [" ", "\n"]):
            self.index += 1
        return self.hdl[old: self.index]

    def consume_decimal(self) -> int:
        while self.index < len(self.hdl) and self.hdl[self.index].isdecimal():
            self.index += 1
        return self.index

    def consume_pin_name(self) -> str:
        old = self.index
        token = self.consume_token()
        if old == self.index:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected pin name")
        return token

    def consume_chip_name(self) -> str:
        old = self.index
        token = self.consume_token()
        if old == self.index:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Expected GateClass name")
        return token

    def consume_expected_token(self, token: str) -> int:
        old = self.index
        self.consume_token()
        if self.hdl[old: self.index] != token:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Missing '{token}' keyword")
        return self.index

    def consume_expected_symbol(self, symbol: str) -> int:
        old = self.index
        self.consume_symbol()
        if self.hdl[old: self.index] != symbol:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Missing '{symbol}'")
        return self.index

    def parse_declaration(self) -> int:
        # consume 'CHIP' keyword
        self.consume_expected_token("CHIP")
        self.advance()

        # consume chip name
        chip_name = self.consume_token()
        if len(chip_name) == 0:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: Missing chip name")
        self.advance()

        # consume '{' symbol
        self.consume_expected_symbol("{")
        self.advance()

        # parse chip program
        self.parse_program()
        self.advance()

        # consume '}' symbol
        self.consume_expected_symbol("}")
        self.advance()

        return self.index

    def parse_program(self) -> int:
        # parse chip interface
        self.parse_interface()
        self.advance()

        # parse chip implementation
        self.parse_implementation()
        self.advance()
        return self.index

    def parse_interface(self) -> int:
        # parse input pins
        self.parse_input_interface()
        self.advance()

        # parse output pins
        self.parse_output_interface()
        self.advance()
        return self.index

    def parse_input_interface(self) -> int:
        self.consume_expected_token("IN")
        self.advance()
        self.input_pins = self.parse_interface_pins()
        return self.index

    def parse_output_interface(self) -> int:
        self.consume_expected_token("OUT")
        self.advance()
        self.output_pins = self.parse_interface_pins()
        return self.index

    def parse_interface_pins(self) -> list[Pin]:
        pins: list[Pin] = []
        while self.peek() != ";":
            # parse & save pin name
            pin = self.parse_interface_pin_token()
            pins.append(pin)
            self.advance()

            if self.peek() == ";":
                break

            # parse ',' symbol
            self.consume_expected_symbol(",")
            self.advance()

        # parse ';' symbol
        self.consume_expected_symbol(";")
        self.advance()
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

        # consume ']' symbol
        self.consume_expected_symbol("]")

        # check if pin width is numeric
        if not width.isnumeric() or not int(width) > 0:
            raise Exception(f"Line {self.hdl.count("\n", 0, self.index)}: {pin_name}[{width}] has invalid bus width")

        return Pin(pin_name, int(width))

    def parse_implementation(self) -> int:
        self.consume_expected_token("PARTS:")
        self.advance()

        while self.peek() != "}":
            self.parse_chip_part()
            self.advance()

        return self.index

    def parse_chip_part(self) -> int:
        chip_name = self.consume_chip_name()
        self.advance()

        self.consume_expected_symbol("(")
        self.advance()

        while self.peek() != ")":
            self.parse_connection()
            self.advance()

            if self.peek() == ")":
                break

            self.consume_expected_symbol(",")
            self.advance()

        self.consume_expected_symbol(")")
        self.advance()

        return self.index

    def parse_connection(self) -> int:
        self.parse_implementation_pin_token(False)
        self.advance()

        self.consume_expected_symbol("=")
        self.advance()

        self.parse_implementation_pin_token(True)
        self.advance()

        return self.index

    def parse_implementation_pin_token(self, right: bool):
        chip_name = self.consume_chip_name()

        if right and chip_name in ["true", "false"]:
            return self.index

        if self.peek() != "[":
            return self.index

        self.consume_expected_symbol("[")

        return None
