# HDL Parser and Chip Testing Framework

- A parser and automated test runner for a simplified subset of the nand2tetris Hardware Description Language (HDL). 
- Given a chip's .hdl file, the program builds an internal model of the chip (recursively resolving any sub-chips it references), simulates its combinational logic for arbitrary inputs, and checks its behavior against a set of expected input/output test vectors.

---

## Usage

### Test a single chip

To test single chip, run following command from project **root** directory:

```bash
python3 -m hdl_parser run <path-to-chip>.hdl <path-to-tests>.tst
```

### Test multiple chips

To test multiple chips placed inside common directory, run following command from project **root** directory:

```bash
python3 -m hdl_parser run-all <path-to-directory>
```

---
