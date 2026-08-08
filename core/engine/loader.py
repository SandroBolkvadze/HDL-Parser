from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, Optional

class ChipLoader(Protocol):
    def path_for(self, chip_name: str) -> Optional[str]:
        pass

    def load(self, chip_name: str) -> str:
        pass

@dataclass
class DefaultChipLoader:
    parent: Path

    def path_for(self, chip_name: str) -> Optional[str]:
        for file in self.parent.rglob("*"):
            if file.is_file() and str(file.name) == f"{chip_name}.hdl":
                return str(file)
        return None

    def load(self, chip_name: str) -> str:
        file = self.path_for(chip_name)
        if file is None:
            raise Exception(f"Chip {chip_name}.hdl not found")
        return Path(file).read_text(encoding="utf-8")
