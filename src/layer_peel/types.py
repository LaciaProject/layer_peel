from typing import (
    Protocol,
    runtime_checkable,
    Callable,
    Iterable,
    Optional,
    Generator,
    Any,
    Iterator,
)
from dataclasses import dataclass


@runtime_checkable
class RawIOBase(Protocol):
    def read(self, size: int | None = -1, /) -> bytes: ...
    def seek(self, pos: int, whence: int = 0, /) -> int: ...


@dataclass
class ExtractConfig:
    lifespan_manager: Callable
    extract_funcs: dict[
        Callable[[bytes], bool],
        Callable[
            [Iterable[bytes], Optional[int]],
            Generator[tuple[bytes, int, Iterator[bytes]], Any, None],
        ],
    ]
    chunk_size: int = 65536
    format_path: Callable[[str], str] = lambda x: f"{x}!"
