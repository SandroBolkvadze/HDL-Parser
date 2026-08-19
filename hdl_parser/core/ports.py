from pathlib import Path
from typing import Protocol


class Loader(Protocol):
    def search_for(self, file: str) -> Path | None:
        pass

    def load(self, file: str) -> str:
        pass
