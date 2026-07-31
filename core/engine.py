from __future__ import annotations

class Engine:
    def __init__(self, hdl: str) -> None:
        self.hdl = hdl
        self.index = 0

    def advance(self) -> None:
        while self.index < len(self.hdl):
            if self.hdl[self.index] in [" ", "\n"]:
                self.index += 1
            if self.hdl[self.index] == "/":
                self.parse_comment()

    def parse_comment_to_end_line(self) -> None:
        assert self.hdl[self.index: self.index + 2] == "//"
        self.index = self.hdl.find("\n", self.index + 2) + 1

    def parse_comment_until_close(self) -> None:
        assert self.hdl[self.index: self.index + 2] == "/*"
        self.index = self.hdl.find("*/", self.index + 2) + 2

    def parse_comment(self) -> None:
        assert self.hdl[self.index] == "/"

        if self.hdl[self.index + 1] == "/":
            self.parse_comment_to_end_line()

        if self.hdl[self.index + 1] == "*":
            self.parse_comment_until_close()

