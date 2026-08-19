from __future__ import annotations

from hdl_parser.core.chips.atomic_chip import ATOMIC_CHIPS
from hdl_parser.core.chips.chip import Chip
from hdl_parser.core.chips.circuit_chip import CircuitChip
from hdl_parser.core.engine.chip_parser import ChipParser
from hdl_parser.core.ports import Loader


class ChipBuilder:
    loader: Loader
    parser: ChipParser

    def __init__(self, loader: Loader, parser: ChipParser) -> None:
        self.loader = loader
        self.parser = parser
        self.cache: dict[str, Chip] = {}

    def build(self, chip_name: str) -> Chip:
        chip_file = f"{chip_name}.hdl"
        if self.loader.path_for(chip_file) is None:
            return ATOMIC_CHIPS[chip_name]

        hdl = self.loader.load(chip_file)
        chip_description = self.parser.parse(hdl)

        chips: dict[str, Chip] = {}
        for chip_part in chip_description.chip_parts:
            if chip_part.chip_name not in self.cache:
                self.cache[chip_part.chip_name] = self.build(chip_part.chip_name)
            chips[chip_part.chip_name] = self.cache[chip_part.chip_name]

        return CircuitChip(
            chip_description.chip_name,
            chip_description.input_pins,
            chip_description.output_pins,
            chip_description.chip_parts,
            chips,
        )
