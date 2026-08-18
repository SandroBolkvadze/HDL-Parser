from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DefaultLoader:
    parent: Path

    def search_for(self, file: str) -> Optional[Path]:
        filepath = self.parent / file
        return filepath if filepath.is_file() else None

    def load(self, file: str) -> str:
        filepath = self.parent / file
        if filepath is None:
            raise Exception(f"File {file} not found")
        return filepath.read_text(encoding="utf-8")
