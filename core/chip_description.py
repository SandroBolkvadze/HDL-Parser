from __future__ import annotations

from dataclasses import dataclass

from core.connection import Connection
from core.pin import Pin

@dataclass
class ChipPart:
    chip_name: str
    chip_connections: list[Connection]

@dataclass
class ChipDescription:
    chip_name: str
    input_pins: list[Pin]
    output_pins: list[Pin]
    chip_parts: list[ChipPart]
