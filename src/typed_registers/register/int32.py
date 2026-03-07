from typing import Self
from dataclasses import dataclass

from .base import Register


@dataclass(slots=True, frozen=True)
class Int32Register(Register):
    WIDTH = 4

    value: int = 0  # signed 32-bit

    def __post_init__(self) -> None:
        if not (-(2**31) <= self.value < 2**31):
            raise ValueError("Value out of signed 32-bit range")

    def to_bytes(self) -> bytes:
        v = self.value & 0xFFFFFFFF
        return bytes(
            [
                (v >> 24) & 0xFF,
                (v >> 16) & 0xFF,
                (v >> 8) & 0xFF,
                v & 0xFF,
            ]
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        cls._assert_data_width(data)
        val = (data[0] << 24) | (data[1] << 16) | (data[2] << 8) | data[3]

        # sign extend
        if val & 0x80000000:
            val -= 1 << 32

        return cls(value=val)
