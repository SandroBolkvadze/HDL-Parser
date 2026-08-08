from pathlib import Path

from core.engine.loader import DefaultChipLoader
from core.engine.parser import DefaultParseEngine

if __name__ == "__main__":
    engine = DefaultParseEngine(DefaultChipLoader(Path("/home/sandro/code/nand2tetris/HDL-Parser/test")))
    engine.parse("And")

    print(engine.chip_name)
    print(engine.input_pins)
    print(engine.output_pins)
    print(engine.chip_parts)
