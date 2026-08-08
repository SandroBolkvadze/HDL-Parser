from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from core.chip import Chip
from core.chip_part import ChipPart

@dataclass
class CircuitChip:
    chip_name: str
    input_pins: list[str]
    output_pins: list[str]
    chip_parts: list[ChipPart]
    chips: dict[str, Chip]

    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass
