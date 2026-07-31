from __future__ import annotations

from poetry.installation.executor import Executor


class Engine:
    def __init__(self, hdl: str) -> None:
        self.hdl = hdl
        self.chip_name = None

    def build(self) -> None:
        self.parse_declaration(self.advance(0))

    def advance(self, index: int) -> int:
        while index < len(self.hdl):
            if self.hdl[index] in [" ", "\n"]:
                index += 1
            elif self.hdl[index] == "/":
                self.consume_comment(index)
            else:
                break
        return index

    def consume_comment_to_end_line(self, index: int) -> int:
        if self.hdl.find("//", index, index + 2) != index:
            raise Exception("Expected comment starting with '//'")
        tmp = self.hdl.find("\n", index + 2)
        if tmp == -1:
            raise Exception("Expected comment to end with 'newline'")
        return tmp + 1

    def consume_comment_until_close(self, index: int) -> int:
        if self.hdl.find("/*", index, index + 2) != index:
            raise Exception("Expected comment starting with '/*'")
        tmp = self.hdl.find("*/", index + 2)
        if tmp == -1:
            raise Exception("Expected comment to end with '*/'")
        return tmp + 2

    def consume_comment(self, index: int) -> int:
        if index + 1 >= len(self.hdl) or self.hdl[index] != "/":
            return index

        if self.hdl[index + 1] == "/":
            return self.consume_comment_to_end_line(index)

        if self.hdl[index + 1] == "*":
            return self.consume_comment_until_close(index)

        return index

    def consume_token(self, index: int) -> int:
        while index < len(self.hdl) and self.hdl[index].isalnum():
            index += 1
        return index

    def consume_symbol(self, index: int) -> int:
        if index < len(self.hdl) and not self.hdl[index].isalnum():
            index += 1
        return index

    def consume_expected_token(self, index: int, token: str) -> int:
        tmp = self.consume_token(index)
        if self.hdl[index: tmp] != token:
            raise Exception(f"Missing '{token}' keyword")
        return tmp

    def consume_expected_symbol(self, index: int, symbol: str) -> int:
        tmp = self.consume_symbol(index)
        if self.hdl[index: tmp] != symbol:
            raise Exception(f"Missing '{symbol}'")
        return tmp

    def parse_declaration(self, index: int) -> int:
        # consume 'CHIP' keyword
        index = self.consume_expected_token(index, "CHIP")
        index = self.advance(index)

        # consume chip name
        tmp = self.consume_token(index)
        if index == tmp:
            raise Exception("Missing chip name")
        self.chip_name = self.hdl[index: tmp]
        index = self.advance(tmp)

        # consume '{' symbol
        index = self.consume_expected_symbol(index, "{")
        index = self.advance(index)

        # parse chip implementation
        index = self.parse_implementation(index)
        index = self.advance(index)

        # consume '}' symbol
        index = self.consume_expected_symbol(index, "}")
        index = self.advance(index)

        return index

    def parse_implementation(self, index: int) -> int:
        return index





