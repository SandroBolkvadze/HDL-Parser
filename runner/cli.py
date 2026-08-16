from pathlib import Path

from typer import Typer

from core.engine.builder import ChipBuilder
from core.engine.parser import DefaultChipParser
from infra.loader import DefaultLoader

from runner.tester import TestParser, run_testcases

cli = Typer(
    name="HDL Parser",
    no_args_is_help=True,
    add_completion=False,
)

@cli.command("test_chip", no_args_is_help=True)
def test(chip_path_str: str, test_path_str: str) -> None:
    chip_path = Path(chip_path_str)
    test_path = Path(test_path_str)

    chip = ChipBuilder(DefaultLoader(chip_path.parent), DefaultChipParser()).build(
        chip_path.stem
    )
    testcases = TestParser(DefaultLoader(test_path.parent).load(test_path.name)).parse()

    run_testcases(chip, testcases)
