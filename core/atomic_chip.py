from __future__ import annotations

class Nand:
    pass

class Not:
    pass

class And:
    pass

class Or:
    pass

ATOMIC_CHIPS = {
    "Nand": Nand(),
    "Not": Not(),
    "And": And(),
    "Or": Or(),
}
