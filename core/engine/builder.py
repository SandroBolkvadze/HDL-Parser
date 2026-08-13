from __future__ import annotations

from dataclasses import dataclass, field

from core.chips.atomic_chip import ATOMIC_CHIPS
from core.chips.chip import Chip
from core.chips.circuit_chip import CircuitChip
from core.engine.parser import ChipParser
from infra.loader import Loader


@dataclass
class ChipBuilder:
    parser: ChipParser
    loader: Loader

    def build(self, chip_name: str) -> Chip:
        if self.loader.search_for(chip_name) is None:
            return ATOMIC_CHIPS[chip_name]

        hdl = self.loader.load(chip_name)
        chip_description = self.parser.parse(hdl)

        chips: dict[str, Chip] = {}
        for chip_part in chip_description.chip_parts:
            chips[chip_part.chip_name] = self.build(chip_part.chip_name)

        return CircuitChip(chip_description.chip_name, chip_description.input_pins, chip_description.output_pins, chip_description.chip_parts, chips)