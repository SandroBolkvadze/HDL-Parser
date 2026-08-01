from dataclasses import dataclass
from core.connection import Connection

@dataclass
class ChipPart:
    chip_name: str
    connections: list[Connection]