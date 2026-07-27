from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Mapping

class PinNotFoundError(Exception):
    pass

class Chip(Protocol):
    def forward(self, **kwargs) -> Mapping[str, int]:
        pass

@dataclass
class ChipNode:
    chip: Chip
    neighbors: list[ChipNode]

@dataclass
class AndChip:
    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        a = kwargs["a"]
        b = kwargs["b"]
        return a & b

@dataclass
class CircuitChip:
    nodes: list[ChipNode]
