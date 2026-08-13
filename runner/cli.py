from typer import Typer, echo

cli = Typer(
    name="HDL Parser",
    no_args_is_help=True,
    add_completion=False,
)

@cli.command("test", no_args_is_help=True)
def test(chip_path: str, test_path: str) -> None:
    pass



