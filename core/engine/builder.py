from __future__ import annotations

from dataclasses import dataclass

from core.chips.atomic_chip import ATOMIC_CHIPS
from core.chips.chip import Chip
from core.chips.circuit_chip import CircuitChip
from core.engine.parser import ChipParser
from infra.loader import Loader


@dataclass
class ChipBuilder:
    loader: Loader
    parser: ChipParser

    def build(self, chip_name: str) -> Chip:
        chip_file = f"{chip_name}.hdl"
        if self.loader.search_for(chip_file) is None:
            return ATOMIC_CHIPS[chip_name]

        hdl = self.loader.load(chip_file)
        chip_description = self.parser.parse(hdl)

        chips: dict[str, Chip] = {}
        for chip_part in chip_description.chip_parts:
            chips[chip_part.chip_name] = self.build(chip_part.chip_name)

        return CircuitChip(
            chip_description.chip_name,
            chip_description.input_pins,
            chip_description.output_pins,
            chip_description.chip_parts,
            chips,
        )
