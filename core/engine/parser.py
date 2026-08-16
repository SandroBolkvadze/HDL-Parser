from __future__ import annotations

from typing import Protocol

from core.chips.chip_description import ChipDescription
from core.chips.chip_part import ChipPart, Connection


class ChipParser(Protocol):
    def parse(self, hdl: str) -> ChipDescription:
        pass


class DefaultChipParser:
    def __init__(self) -> None:
        self.hdl = ""
        self.index = 0
        self.chip_description = ChipDescription()

    def reset(self, hdl: str) -> None:
        self.hdl = hdl
        self.index = 0
        self.chip_description = ChipDescription()

    def parse(self, hdl: str) -> ChipDescription:
        self.reset(hdl)
        self.parse_declaration()
        return self.chip_description

    def peek(self) -> str:
        self.advance()
        return self.hdl[self.index] if self.index < len(self.hdl) else ""

    def advance(self) -> int:
        while self.index < len(self.hdl):
            if self.hdl[self.index] in [" ", "\t", "\n"]:
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
        tmp = self.hdl.find("\n", self.index + 1)
        self.index = tmp + 1 if tmp != -1 else len(self.hdl)
        return self.index

    def consume_comment_until_close(self) -> int:
        tmp = self.hdl.find("*/", self.index + 2)
        self.index = tmp + 2 if tmp != -1 else len(self.hdl)
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
        if self.index < len(self.hdl) and not self.hdl[self.index].isalnum():
            self.index += 1
        return self.hdl[old : self.index]

    def parse_declaration(self) -> int:
        # consume 'CHIP' keyword
        self.consume_token()

        # consume chip name
        self.chip_description.chip_name = self.consume_token()

        # consume '{' symbol
        self.consume_symbol()

        # parse chip program
        self.parse_program()

        # consume '}' symbol
        self.consume_symbol()

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
        # consume 'IN' keyword
        self.consume_token()
        self.chip_description.input_pins = self.parse_interface_pins()
        return self.index

    def parse_output_interface(self) -> int:
        # consume 'OUT' keyword
        self.consume_token()
        self.chip_description.output_pins = self.parse_interface_pins()
        return self.index

    def parse_interface_pins(self) -> list[str]:
        pins: list[str] = []

        while self.peek() != ";":
            # parse & save pin name
            pins.append(self.consume_token())

            if self.peek() == ";":
                break

            # parse ',' symbol
            self.consume_symbol()

        # parse ';' symbol
        self.consume_symbol()
        return pins

    def parse_implementation(self) -> int:
        self.consume_token()

        self.consume_symbol()

        while self.peek() != "}":
            self.chip_description.chip_parts.append(self.parse_chip_part())

        return self.index

    def parse_chip_part(self) -> ChipPart:
        chip_name = self.consume_token()

        self.consume_symbol()

        connections: list[Connection] = []

        while self.peek() != ")":
            connections.append(self.parse_connection())
            if self.peek() == ")":
                break
            self.consume_symbol()

        self.consume_symbol()

        self.consume_symbol()

        return ChipPart(chip_name, connections)

    def parse_connection(self) -> Connection:
        # parse left pin
        left = self.consume_token()

        # consume '='
        self.consume_symbol()

        # parse right pin
        right = self.consume_token()

        return Connection(left, right)
