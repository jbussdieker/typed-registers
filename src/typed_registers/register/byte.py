from abc import abstractmethod
from dataclasses import dataclass

from .base import Register, R


@dataclass(slots=True, frozen=True)
class ByteRegister(Register):
    WIDTH = 1

    @abstractmethod
    def to_byte(self) -> int: ...

    @classmethod
    @abstractmethod
    def from_byte(cls: type[R], data: int) -> R: ...

    def to_bytes(self) -> bytes:
        return bytes([self.to_byte()])

    @classmethod
    def from_bytes(cls: type[R], data: bytes) -> R:
        cls._assert_data_width(data)
        return cls.from_byte(data[0])
