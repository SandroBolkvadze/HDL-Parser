from __future__ import annotations

from dataclasses import dataclass

from core.chips.chip import Chip


@dataclass
class Testcase:
    inputs: dict[str, int]
    expected: dict[str, int]


@dataclass
class TestParser:
    tests: str

    def parse(self) -> list[Testcase]:
        ins_pins: list[str] = []
        outs_pins: list[str] = []
        testcases: list[Testcase] = []

        tests = [
            line.strip() for line in self.tests.splitlines() if len(line.strip()) > 0
        ]

        for i, line in enumerate(tests):
            inputs, outputs = line.split(";")
            ins_str = [elem.strip() for elem in inputs.split(",")]
            outs_str = [elem.strip() for elem in outputs.split(",")]
            if i == 0:
                ins_pins = ins_str
                outs_pins = outs_str
                continue

            ins_int = [int(elem) for elem in ins_str]
            outs_int = [int(elem) for elem in outs_str]
            testcases.append(
                Testcase(
                    dict(zip(ins_pins, ins_int)),
                    dict(zip(outs_pins, outs_int)),
                )
            )

        return testcases


def run_testcases(chip: Chip, testcases: list[Testcase]) -> None:
    passed = 0
    for i, testcase in enumerate(testcases):
        outputs = chip.forward(testcase.inputs)
        if outputs == testcase.expected:
            passed += 1
            print(f"Testcase {i} passed")
        else:
            print(f"Testcase {i} failed; expected {testcase.expected}; got {outputs}")

    print(f"Testcases passed {passed} / {len(testcases)}")
