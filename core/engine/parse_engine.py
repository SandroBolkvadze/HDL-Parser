from __future__ import annotations

from typing import Protocol

from pygments.lexers import hdl

from core.chip_description import ChipPart
from core.connection import Connection
from core.pin import Pin


class ParseEngine(Protocol):
    def parse(self, hdl: str) -> None:
        pass

class DefaultParseEngine:
    def __init__(self):
        self.hdl = ""
        self.index = 0
        self.chip_name = ""
        self.input_pins: list[str] = []
        self.output_pins: list[str] = []
        self.chip_parts: list[ChipPart] = []

    def reset(self, hdl: str) -> None:
        self.hdl = hdl
        self.index = 0
        self.chip_name = ""
        self.input_pins: list[Pin] = []
        self.output_pins: list[Pin] = []
        self.chip_parts: list[ChipPart] = []

    def parse(self, hdl: str) -> None:
        self.reset(hdl)
        self.parse_declaration()

    def peek(self) -> str:
        self.advance()
        return self.hdl[self.index] if self.index < len(self.hdl) else ""

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

    def consume_comment(self) -> int:
        if self.hdl[self.index + 1] == "*":
            self.consume_comment_until_close()
        else:
            self.consume_comment_to_end_line()

        return self.index

    def consume_comment_to_end_line(self) -> int:
        self.index = self.hdl.find("\n", self.index + 2) + 1
        return self.index

    def consume_comment_until_close(self) -> int:
        tmp = self.hdl.find("*/", self.index + 2)
        self.index = tmp + 2 if tmp != -1 else len(hdl)
        return self.index

    def consume_token(self) -> str:
        self.advance()
        old = self.index
        if self.index < len(self.hdl) and self.hdl[self.index].isalpha():
            self.index += 1
            while self.index < len(self.hdl) and self.hdl[self.index].isalnum():
                self.index += 1
        return self.hdl[old : self.index]

    def consume_symbol(self) -> str:
        self.advance()
        old = self.index
        if self.index < len(self.hdl) and (
            not self.hdl[self.index].isalnum()
        ):
            self.index += 1
        return self.hdl[old : self.index]

    def consume_nonempty_token(self, err: str) -> str:
        token = self.consume_token()
        if len(token) == 0:
            raise Exception(f"Line {self.hdl.count('\n', 0, self.index)}: {err}")
        return token

    def consume_expected_token(self, expected_token: str) -> str:
        token = self.consume_token()
        if token != expected_token:
            raise Exception(
                f"Line {self.hdl.count('\n', 0, self.index)}: Missing '{expected_token}' keyword"
            )
        return token

    def consume_expected_symbol(self, expected_symbol: str) -> str:
        symbol = self.consume_symbol()
        if symbol != expected_symbol:
            raise Exception(
                f"Line {self.hdl.count('\n', 0, self.index)}: Missing '{expected_symbol}'"
            )
        return symbol

    def parse_declaration(self) -> int:
        # consume 'CHIP' keyword
        self.consume_expected_token("CHIP")

        # consume chip name
        self.chip_name = self.consume_nonempty_token("Missing chip name")

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

    def parse_interface_pins(self) -> list[str]:
        pins: list[str] = []

        while self.peek() != ";":
            # parse & save pin name
            pins.append(self.consume_nonempty_token("Pin name expected"))

            if self.peek() == ";":
                break

            # parse ',' symbol
            self.consume_expected_symbol(",")

        # parse ';' symbol
        self.consume_expected_symbol(";")
        return pins

    def parse_implementation(self) -> int:
        self.consume_expected_token("PARTS")

        self.consume_expected_symbol(":")

        while self.peek() != "}":
            self.chip_parts.append(self.parse_chip_part())

        return self.index

    def parse_chip_part(self) -> ChipPart:
        chip_name = self.consume_nonempty_token("A GateClass name is expected")

        self.consume_expected_symbol("(")

        connections: list[Connection] = []

        while self.peek() != ")":
            connections.append(self.parse_connection())
            if self.peek() == ")":
                break
            self.consume_expected_symbol(",")

        self.consume_expected_symbol(")")

        self.consume_expected_symbol(";")

        return ChipPart(chip_name, connections)

    def parse_connection(self) -> Connection:
        left = self.consume_nonempty_token("A pin name is expected")
        self.consume_expected_symbol("=")
        right = self.consume_nonempty_token("A pin name is expected")

        return Connection(left, right)
