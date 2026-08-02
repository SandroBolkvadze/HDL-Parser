from dataclasses import dataclass
from typing import Tuple


@dataclass
class SubBus:
    pin_name: str
    pin_sub_bus: Tuple[int, int]


@dataclass
class Connection:
    left: SubBus
    right: SubBus


@dataclass
class ChipConnection:
    chip_name: str
    connection: Connection
