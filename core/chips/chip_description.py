from dataclasses import dataclass, field

from core.chips.chip_part import ChipPart


@dataclass
class ChipDescription:
    chip_name: str = ""
    input_pins: list[str] = field(default_factory=list)
    output_pins: list[str] = field(default_factory=list)
    chip_parts: list[ChipPart] = field(default_factory=list)
