from pathlib import Path

from core.chip import Chip
from core.engine.parse_engine import ParseEngine


class BuildEngine:
    def __init__(self, parser: ParseEngine):
        self.parser = parser

    def build(self, hdl: Path) -> Chip:
        
        pass
