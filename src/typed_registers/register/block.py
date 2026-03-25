from typing import TypeVar
from dataclasses import dataclass
from abc import abstractmethod

from .base import Register

B = TypeVar("B", bound="BlockRegister")


@dataclass(slots=True, frozen=True)
class BlockRegister(Register):

    @classmethod
    def from_bytes(cls: type[B], data: bytes) -> B:
        cls._assert_data_width(data)
        return cls._decode(data)

    @classmethod
    @abstractmethod
    def _decode(cls: type[B], data: bytes) -> B: ...

    def to_bytes(self) -> bytes:
        return self._encode()

    def _encode(self) -> bytes:
        raise TypeError(f"{type(self).__name__} does not support encoding")
