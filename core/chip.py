from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Mapping

from core.chip_description import ChipPart, ChipDescription
from core.pin import Pin

class Chip(Protocol):
    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass

@dataclass
class CircuitChip:
    chip_name: str
    input_pins: list[Pin]
    output_pins: list[Pin]
    chip_parts: list[ChipPart]
    chips: list[CircuitChip]

    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass
