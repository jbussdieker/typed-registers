from typing import Self
from dataclasses import dataclass

from .base import Register


@dataclass(slots=True, frozen=True)
class Int24Register(Register):
    WIDTH = 3

    value: int = 0  # signed 24-bit

    def __post_init__(self) -> None:
        if not (-(2**23) <= self.value < 2**23):
            raise ValueError("Value out of signed 24-bit range")

    def to_bytes(self) -> bytes:
        v = self.value & 0xFFFFFF
        return bytes(
            [
                (v >> 16) & 0xFF,
                (v >> 8) & 0xFF,
                v & 0xFF,
            ]
        )

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        cls._assert_data_width(data)
        val = (data[0] << 16) | (data[1] << 8) | data[2]

        # sign extend
        if val & 0x800000:
            val -= 1 << 24

        return cls(value=val)
