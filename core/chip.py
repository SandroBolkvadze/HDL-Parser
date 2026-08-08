from __future__ import annotations

from typing import Protocol


class Chip(Protocol):
    def get_input_pins(self) -> list[str]:
        pass

    def get_output_pins(self) -> list[str]:
        pass

    def forward(self, inputs: dict[str, int]) -> dict[str, int]:
        pass
