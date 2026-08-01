from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Mapping

class Chip(Protocol):
    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass

@dataclass
class Pin:
    pin:  str
    chip: Chip

@dataclass
class AndChip:
    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        a = kwargs["a"]
        b = kwargs["b"]
        return a & b

@dataclass
class CircuitChip:
    ins:   list[str]
    outs:  list[str]
    nodes: list[Chip]
    edges: dict[str, list[Pin]]

    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass

