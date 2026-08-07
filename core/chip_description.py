from __future__ import annotations

from dataclasses import dataclass

from core.connection import Connection
from core.pin import Pin

@dataclass
class ChipPart:
    chip_name: str
    chip_connections: list[Connection]
