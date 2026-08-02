from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class File:
    path: Path

    def load(self) -> str:
        with self.path.open("r", newline="\n") as file:
            content = "".join(line for line in file)
            return content

    def save(self, lines: Iterable[str]) -> None:
        with self.path.open("w") as file:
            for line in lines:
                file.write(line)
