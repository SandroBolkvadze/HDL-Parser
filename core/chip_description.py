from __future__ import annotations

from dataclasses import dataclass

from core.connection import ChipConnection
from core.pin import Pin


@dataclass
class ChipDescription:
    chip_name: str
    input_pins: list[Pin]
    output_pins: list[Pin]
    chip_parts: list[str]
    chip_connections: list[ChipConnection]
