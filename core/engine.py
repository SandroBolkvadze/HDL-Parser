from __future__ import annotations

class Engine:
    def __init__(self, hdl: str) -> None:
        self.hdl = hdl

        self.line = 1
        self.index = 0

        self.chip_name = None
        self.input_pins = []
        self.output_pins = []

    def parse(self) -> None:
        self.advance()
        self.parse_declaration()

    def advance(self) -> int:
        while self.index < len(self.hdl):
            if self.hdl[self.index] == " ":
                self.index += 1
            elif self.hdl[self.index] == "\n":
                self.index += 1
                self.line += 1
            elif self.hdl[self.index] == "/":
                # print("here", self.index, self.hdl[self.index: self.index+10])
                self.consume_comment()
            else:
                break
        return self.index

    def peek(self) -> str:
        return self.hdl[self.index] if self.index < len(self.hdl) else ""

    def consume_comment_to_end_line(self) -> int:
        if self.hdl.find("//", self.index) != self.index:
            raise Exception(f"Line {self.line}: Expected comment starting with '//'")
        tmp = self.hdl.find("\n", self.index + 2)
        if tmp == -1:
            raise Exception(f"Line {self.line}: Expected comment to end with 'newline'")
        self.line += 1
        self.index = tmp + 1
        return self.index

    def consume_comment_until_close(self) -> int:
        if self.hdl.find("/*", self.index) != self.index:
            raise Exception(f"Line {self.line}: Expected comment starting with '/*'")
        tmp = self.hdl.find("*/", self.index + 2)
        if tmp == -1:
            raise Exception(f"Line {self.line}: Expected comment to end with '*/'")
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

    def consume_token(self) -> int:
        if self.index < len(self.hdl) and self.hdl[self.index].isalpha():
            self.index += 1
            while self.index < len(self.hdl) and self.hdl[self.index].isalnum():
                self.index += 1
        return self.index

    def consume_symbol(self) -> int:
        if self.index < len(self.hdl) and (not self.hdl[self.index].isalnum() and not self.hdl[self.index] in [" ", "\n"]):
            self.index += 1
        return self.index

    def consume_pin_token(self):
        old = self.index
        self.consume_token()
        if old == self.index:
            raise Exception(f"Line {self.line}: Expected pin name")
        return self.index

    def consume_expected_token(self, token: str) -> int:
        old = self.index
        self.consume_token()
        if self.hdl[old: self.index] != token:
            raise Exception(f"Line {self.line}: Missing '{token}' keyword")
        return self.index

    def consume_expected_symbol(self, symbol: str) -> int:
        old = self.index
        self.consume_symbol()
        if self.hdl[old: self.index] != symbol:
            raise Exception(f"Line {self.line}: Missing '{symbol}'")
        return self.index

    def parse_declaration(self) -> int:
        # consume 'CHIP' keyword
        self.consume_expected_token("CHIP")
        self.advance()

        # consume chip name
        old = self.index
        self.consume_token()
        if old == self.index:
            raise Exception(f"Line {self.line}: Missing chip name")
        self.chip_name = self.hdl[old: self.index]
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
        self.parse_pins()
        return self.index

    def parse_output_interface(self) -> int:
        self.consume_expected_token("OUT")
        self.advance()
        self.parse_pins()
        return self.index

    def parse_pins(self):
        while self.peek() != ";":
            old = self.index
            self.consume_pin_token()
            self.input_pins.append(self.hdl[old: self.index])
            self.advance()

            if self.peek() == ";":
                break

            self.consume_expected_symbol(",")
            self.advance()

        self.consume_expected_symbol(";")
        self.advance()
        return self.index

    def parse_implementation(self) -> int:
        pass





