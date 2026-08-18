from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChipPart:
    chip_name: str
    chip_connections: list[Connection]


@dataclass
class Connection:
    left: str
    right: str
