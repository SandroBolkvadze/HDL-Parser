from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict

from core.chip import Chip
from core.chip_part import ChipPart
from core.utils import topo_sort

@dataclass
class CircuitChip:
    chip_name: str
    input_pins: list[str]
    output_pins: list[str]
    chip_parts: list[ChipPart]
    chips: dict[str, Chip]

    def get_input_pins(self) -> list[str]:
        return self.input_pins

    def get_output_pins(self) -> list[str]:
        return self.output_pins

    def forward(self, inputs: dict[str, int]) -> dict[str, int]:
        nodes = [i for i in range(len(self.chip_parts))]
        graph: DefaultDict[int, list[int]] = defaultdict(list)

        for i, chip_part_i in enumerate(self.chip_parts):
            outs = set([connection.right for connection in chip_part_i.chip_connections if connection.left in self.chips[chip_part_i.chip_name].get_output_pins()])
            for j, chip_part_j in enumerate(self.chip_parts):
                if j == i: continue
                ins = set([connection.right for connection in chip_part_j.chip_connections if connection.left in self.chips[chip_part_j.chip_name].get_input_pins()])
                if len(outs & ins): graph[i].append(j)

        topo_sorted_nodes = topo_sort(nodes, graph)
        assert(topo_sorted_nodes is not None)

        resolved: dict[str, int] = inputs | {input_pin: 0 for input_pin in self.input_pins if input_pin not in inputs}

        for i in topo_sorted_nodes:
            chip_part = self.chip_parts[i]

            chip_input: dict[str, int] = {}
            for connection in chip_part.chip_connections:
                if connection.left in self.chips[chip_part.chip_name].get_input_pins():
                    chip_input[connection.left] = resolved[connection.right]

            chip_output = self.chips[chip_part.chip_name].forward(chip_input)
            for connection in chip_part.chip_connections:
                if connection.left in self.chips[chip_part.chip_name].get_output_pins():
                    resolved[connection.right] = chip_output[connection.left]

        return {out_pin: resolved[out_pin] for out_pin in self.output_pins}
