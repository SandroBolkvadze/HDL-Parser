from pathlib import Path

from typer import Typer

from hdl_parser.core.engine.chip_builder import ChipBuilder
from hdl_parser.core.engine.chip_parser import DefaultChipParser
from hdl_parser.infra.loader import DefaultLoader
from hdl_parser.runner.tester import parse_tst, run_testcases

cli = Typer(
    name="HDL Parser",
    no_args_is_help=True,
    add_completion=False,
)


def run(hdl_path: Path, tst_path: Path) -> None:
    chip_parser = DefaultChipParser()
    chip_builder = ChipBuilder(DefaultLoader(hdl_path.parent), chip_parser)

    chip = chip_builder.build(hdl_path.stem)
    testcases = parse_tst(DefaultLoader(tst_path.parent).load(tst_path.name))

    run_testcases(chip, testcases)


@cli.command("run_all_tests")
def run_all_tests() -> None:
    examples = Path(__file__).parent.parent.parent / "examples"
    for hdl_path in examples.glob("*.hdl"):
        print(f"- Running tests on '{hdl_path.stem}'")
        run(hdl_path, hdl_path.with_suffix(".tst"))
        print("#" * 20)


@cli.command("run_test", no_args_is_help=True)
def run_test(hdl_path: Path, tst_path: Path) -> None:
    print(f"- Running tests on '{hdl_path.stem}'")
    run(hdl_path, tst_path)
    print("#" * 20)
