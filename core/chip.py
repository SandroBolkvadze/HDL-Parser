from __future__ import annotations

from typing import Protocol, Mapping


class Chip(Protocol):
    def forward(self, **kwargs: Mapping[str, int]) -> Mapping[str, int]:
        pass
