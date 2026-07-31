from __future__ import annotations

class Engine:
    def __init__(self, hdl: str) -> None:
        self.hdl = hdl

    def peek_advance(self) -> int:

        pass

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
        if self.hdl.find("//", index) != index:
            return index
        tmp = self.hdl.find("\n", index + 2)
        if tmp == -1:
            return index
        return tmp + 1

    def consume_comment_until_close(self, index: int) -> int:
        if self.hdl.find("/*", index) != index:
            return index
        tmp = self.hdl.find("*/", index + 2)
        if tmp == -1:
            return index
        return tmp + 2

    def consume_comment(self, index: int) -> int:
        if index + 1 >= len(self.hdl) or self.hdl[index] != "/":
            return index

        if self.hdl[index + 1] == "/":
            return self.consume_comment_to_end_line(index)

        if self.hdl[index + 1] == "*":
            return self.consume_comment_until_close(index)

        return index

    def consume_keyword(self, index: int, keyword: str) -> int:
        if self.hdl[index: min(index + len(keyword), len(self.hdl))] != keyword:
            return index

        if self.advance(index + len(keyword)) == index + len(keyword):
            return index

        return index + len(keyword)

    def consume_token(self, index: int) -> int:
        while index < len(self.hdl) and (self.hdl[index].isalpha() or self.hdl[index].isnumeric()):
            index += 1
        return index

    def build(self) -> None:
        self.parse_declaration(self.advance(0))

    def parse_declaration(self, index: int) -> None:
        self.consume_keyword(index, "CHIP")
        chip_name = self.consume_token()




