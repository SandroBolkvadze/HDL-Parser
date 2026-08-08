from pathlib import Path

from core.engine.loader import DefaultChipLoader
from core.engine.parser import DefaultParser

if __name__ == "__main__":
    parser = DefaultParser(DefaultChipLoader(Path("/home/sandro/code/nand2tetris/HDL-Parser/test")))
    chip = parser.parse("And")

    print(parser.chip_name)
    print(parser.input_pins)
    print(parser.output_pins)
    print(parser.chip_parts)
    print(parser.chips)

    out = chip.forward({"a": 1, "b": 1})
    print(out)