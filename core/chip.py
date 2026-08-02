from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Mapping

from core.connection import ChipConnection
from core.pin import Pin


class Chip(Protocol):
    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass

@dataclass
class CircuitChip:
    chip_name: str
    ins: list[Pin]
    outs: list[Pin]
    chip_parts: list[CircuitChip]
    chip_connections: list[ChipConnection]

    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass
