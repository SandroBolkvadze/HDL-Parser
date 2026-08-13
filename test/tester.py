from __future__ import annotations

from dataclasses import dataclass, field

from core.chips.chip import Chip
from infra.loader import Loader


@dataclass
class Testcase:
    inputs: dict[str, int]
    expected: dict[str, int]

@dataclass
class TestParser:
    def parse(self, tests: str) -> list[Testcase]:
        ins_pins = []
        outs_pins = []
        testcases: list[Testcase] = []

        tests = [line.strip() for line in tests.splitlines() if len(line.strip()) > 0]

        for i, line in enumerate(tests):
            ins, outs = line.split(";")
            ins = [elem.strip() for elem in ins.split(",")]
            outs = [elem.strip() for elem in outs.split(",")]
            if i == 0:
                ins_pins = ins
                outs_pins = outs
                continue

            ins = [int(elem) for elem in ins]
            outs = [int(elem) for elem in outs]
            testcases.append(Testcase(dict(zip(ins_pins, ins)), dict(zip(outs_pins, outs))))

        return testcases


@dataclass
class TestRunner:

    def run_testcases(self, chip: Chip, testcases: list[Testcase]) -> None:
        passed = 0
        for i, testcase in enumerate(testcases):
            outputs = chip.forward(testcase.inputs)
            if outputs == testcase.expected:
                print(f"Testcase {i} passed")
                passed += 1
            else:
                print(f"Testcase {i} failed; expected {testcase.expected}; got {outputs}")

        print(f"Total passed: {passed} / {len(testcases)}")


