from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

@dataclass
class Nand:
    def get_input_pins(self) -> list[str]:
        return ["a", "b"]

    def get_output_pins(self) -> list[str]:
        return ["out"]

    def forward(self, inputs: Mapping[str, int]) -> Mapping[str, int]:
        a_pin = inputs.get("a", 0)
        b_pin = inputs.get("b", 0)
        return {"out": int(not (a_pin and b_pin))}

@dataclass
class Not:
    def get_input_pins(self) -> list[str]:
        return ["in"]

    def get_output_pins(self) -> list[str]:
        return ["out"]

    def forward(self, inputs: Mapping[str, int]) -> Mapping[str, int]:
        in_pin = inputs.get("in", 0)
        return {"out": int(not in_pin)}

@dataclass
class And:
    def get_input_pins(self) -> list[str]:
        return ["a", "b"]

    def get_output_pins(self) -> list[str]:
        return ["out"]

    def forward(self, inputs: Mapping[str, int]) -> Mapping[str, int]:
        a_pin = inputs.get("a", 0)
        b_pin = inputs.get("b", 0)
        return {"out": int(a_pin and b_pin)}

@dataclass
class Or:
    def get_input_pins(self) -> list[str]:
        return ["a", "b"]

    def get_output_pins(self) -> list[str]:
        return ["out"]

    def forward(self, inputs: Mapping[str, int]) -> Mapping[str, int]:
        a_pin = inputs.get("a", 0)
        b_pin = inputs.get("b", 0)
        return {"out": int(a_pin or b_pin)}

ATOMIC_CHIPS = {
    "Nand": Nand(),
    "Not": Not(),
    "And": And(),
    "Or": Or(),
}
