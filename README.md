# Final: HDL Parser and Chip Testing Framework

## Overview

In this project, you will write a program that **parses syntactically correct HDL files**, builds an internal model of the chip, and **automatically tests** the chip’s behavior against provided input-output test vectors.

---

## Objectives

- Parse HDL files assuming correct syntax.
- Build an internal representation of the chip and its components.
- Simulate chip behavior for given inputs.
- Verify outputs against expected results.
- Produce a test report summarizing pass/fail outcomes.

---

## Built-in Chips

Your HDL parser and simulator **must support** these built-in chips (predefined primitive gates), which are considered atomic and do **not** require further parsing:

| Chip Name  | Description                        | Inputs         | Outputs  |
|------------|------------------------------------|----------------|----------|
| `Nand`     | Logical NAND gate                  | 2              | 1        |
| `Not`      | Logical NOT gate                   | 1              | 1        |
| `And`      | Logical AND gate                   | 2              | 1        |
| `Or`       | Logical OR gate                    | 2              | 1        |


### Notes

- These chips act as primitives during simulation: your program does **not** parse their internals from HDL files.
- Chips beyond this list must be parsed from HDL files and can instantiate these built-ins.
- The inputs and outputs above should match the HDL spec and test vectors.
- Your simulator should correctly implement the logic for each built-in chip.

---

## Handling Non Built-in Chips

When your parser encounters a chip instantiation that is **not** one of the built-in chips (see previous section), it must:

  1. **Locate and parse** the corresponding HDL file for that chip.
  2. Build an internal representation of that chip’s structure by parsing its `IN`, `OUT`, and `PARTS` sections.
  3. Recursively resolve any further chip instantiations within that chip.
  4. Integrate the parsed sub-chip into the simulation model of the parent chip.


### Notes

- Your simulator must correctly simulate such composed chips by invoking the behavior of all sub-chips, down to built-in primitives.
- You can assume the HDL files for all non built-in chips referenced will be available in the same directory as the parent. They will also be syntactically correct.
- No error handling is required for missing files or incorrect syntax, as inputs are guaranteed valid.

---

## Deliverables

1. **HDL Parser and Simulator**
   - Parses HDL files to represent chip structure and connections.
   - Simulates chip logic based on input values.
   - Handles built-in gates (`And`, `Or`, `Not`, `Nand`) and chip instantiations.

2. **Testing Framework**
   - Reads test vectors specifying input values and expected output.
   - Applies input vectors to the chip simulator.
   - Compares actual outputs with expected outputs.
   - Prints a summary report of test case results.

3. **Documentation**
   - How to run your program.
   - Description of your approach.
   - Example HDL and test vector files.

---

## Input and Output Formats

### HDL File (Input)

- HDL files define the chip, inputs, outputs, and parts.
- You can assume valid HDL syntax; no need to check for errors.

### Test Vector File (Input)

Format example (CSV-style):

```CSV
  a,b; out
  0,0; 0
  0,1; 0
  1,0; 0
  1,1; 1
```

- Each line represents one test case with inputs and expected output.

### Program Output

- For each test case, print pass/fail with details.
- At the end, print a summary count: how many tests passed out of total.

---

## Requirements

- Support parsing chips with `IN`, `OUT`, and `PARTS` sections.
- Simulate logic gates and chip instances according to HDL.
- No error handling needed — assume perfect input.

---

## Non-requirements

- Support for multi-bit inputs/outputs is not required.
- Support for Multi-bit busses/sub-busses is not required.
- Support for sequencial chips is not required.

---

## Grading Criteria

| Criteria                  | Points |
|---------------------------|--------|
| Correct parsing of HDL    | 30     |
| Accurate chip simulation  | 40     |
| Correct test output       | 20     |
| Lintting/formatting       | 10     |