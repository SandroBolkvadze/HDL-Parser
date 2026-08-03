from pathlib import Path
from typing import Protocol

from core.chip import Chip
from core.engine.parse_engine import ParseEngine

class HDLLoader(Protocol):
    def load(self, path: Path) -> str:
        pass


class BuildEngine:
    def __init__(self, parser: ParseEngine, loader: HDLLoader):
        self.parser = parser

    def build(self, hdl: Path) -> Chip:

        pass
