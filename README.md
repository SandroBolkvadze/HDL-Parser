# HDL Parser and Chip Testing Framework

- A parser and automated test runner for a simplified subset of the nand2tetris Hardware Description Language (`HDL`). 

- Given a chip's `.hdl` file, the program builds an internal model of the chip (recursively resolving any sub-chips it references), simulates its combinational logic for arbitrary inputs, and checks its behavior against a set of expected input/output test vectors.

---

## How to run project

### Requirements

- Install poetry:
```shell
python -m pip install --upgrade pip
python -m pip install --upgrade poetry
```

- Run inside project:
```shell
poetry install --no-root
```

### Test a single chip

To test single chip, run following command from project **root** directory:

```bash
poetry run python -m hdl_parser run <path-to-chip>.hdl <path-to-tests>.tst
```

### Test multiple chips

To test multiple chips living under some directory, run following command from project **root** directory:

```bash
poetry run python -m hdl_parser run-all <path-to-directory>
```

---

## Description of approach

The project is split into two parts: 

- **Parsing and Building** (`engine` directory): `ChipParser` parses `.hdl` file into `ChipDescription` (`chip_description.py`). `ChipBuilder` utilizes `ChipParser` and `Loader` (for file reading) to build recursive representation of chip given its name.  


- **Chip simulation** (`chips` directory): Every chip - Atomic and Circuit - conforms to same Chip Protocol (`chip.py`) which defines following methods:

```python
def get_input_pins(self) -> list[str]: ...
def get_output_pins(self) -> list[str]: ...
def forward(self, inputs: dict[str, int]) -> dict[str, int]: ...
```

 Each chip's `forward` takes in *pin:value* mapping as input and outputs *pin:value* mapping.
 
 Sub-chips of circuit (non-atomic) chip are *topologically* sorted (`graph.py`) before passing *inputs* through.

```tree
.
├── examples
│   ├── *.hdl
│   └── *.tst
├── hdl_parser/
│   ├── core/
│   │   ├── chips/
│   │   │   ├── atomic_chip.py
│   │   │   ├── chip.py
│   │   │   ├── chip_description.py
│   │   │   ├── chip_part.py
│   │   │   └── circuit_chip.py
│   │   ├── engine/
│   │   │   ├── chip_builder.py
│   │   │   └── chip_parser.py
│   │   ├── general/
│   │   │   └── graph.py
│   │   ├── tester/
│   │   │   └── tester.py
│   │   └── ports.py 
│   ├── infra/
│   │   └── loader.py
│   ├── runner/
│   │   └── cli.py
│   └── __main__.py
├── .gitignore
├── README.md
└── pyproject.toml
```

## Examples HDL and test files

Testing framework is contained in `tester.py`.

Example chips live under `examples/`, ranging from a single level of composition to several levels of recursion and reused sub-chips.

A pair of `.hdl` and `.tst` files under `examples/`:

`examples/Xor.hdl` - a single-level composite chip built entirely from atomic primitives:
```hdl
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/1/Xor.hdl
/**
 * Exclusive-or gate:
 * if ((a and Not(b)) or (Not(a) and b)) out = 1, else out = 0
 */
CHIP Xor {
    IN a, b;
    OUT out;

    PARTS:
    Not(in=a, out=nota);
    Not(in=b, out=notb);
    
    And(a=nota, b=b, out=notaAndb);
    And(a=a, b=notb, out=notbAnda);

    Or(a=notaAndb, b=notbAnda, out=out);
}
```

`examples/Xor.tst`:
```csv
a,b; out
0,0; 0
0,1; 1
1,0; 1
1,1; 0
```

The rest of examples covers deeper recursions, constant (`true`/`false`) pin wiring, etc.
Run `poetry run python -m hdl_parser run-all examples` to test all of them at once.
