from pathlib import Path

from core.engine.loader import DefaultChipLoader
from core.engine.parser import DefaultParser

if __name__ == "__main__":
    parser = DefaultParser(DefaultChipLoader(Path("/home/sandro/code/nand2tetris/HDL-Parser/test")))
    chip = parser.parse("Mux")
    out = chip.forward({"a": 1, "b": 1, "sel": 0})
    print(out)