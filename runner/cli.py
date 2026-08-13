from pathlib import Path

from typer import Typer, echo

from core.engine.builder import ChipBuilder
from core.engine.parser import DefaultChipParser
from infra.loader import DefaultLoader
from test.tester import TestParser, run_testcases

cli = Typer(
    name="HDL Parser",
    no_args_is_help=True,
    add_completion=False,
)

@cli.command("test", no_args_is_help=True)
def test(chip_path: str, test_path: str) -> None:
    chip_path = Path(chip_path)
    test_path = Path(test_path)

    chip = ChipBuilder(DefaultLoader(chip_path.parent), DefaultChipParser()).build(chip_path.name)
    testcases = TestParser(DefaultLoader(test_path.parent).load(test_path.name)).parse()

    run_testcases(chip, testcases)


