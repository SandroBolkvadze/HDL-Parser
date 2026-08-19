from dataclasses import dataclass
from pathlib import Path


@dataclass
class DefaultLoader:
    parent: Path

    def path_for(self, file: str) -> Path | None:
        filepath = self.parent / file
        return filepath if filepath.is_file() else None

    def load(self, file: str) -> str:
        filepath = self.parent / file
        if not filepath.is_file():
            raise Exception(f"File '{file}' not found")
        return filepath.read_text(encoding="utf-8")
