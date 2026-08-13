from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Optional

class Loader(Protocol):
    def search_for(self, file: str) -> Optional[Path]:
        pass

    def load(self, file: str) -> str:
        pass

@dataclass
class DefaultLoader:
    parent: Path

    def search_for(self, file: str) -> Optional[Path]:
        for filepath in self.parent.rglob("*"):
            if filepath.is_file() and str(filepath.name) == file:
                return filepath
        return None

    def load(self, file: str) -> str:
        filepath = self.search_for(file)
        if filepath is None:
            raise Exception(f"File {file} not found")
        return filepath.read_text(encoding="utf-8")
