from typing import ClassVar, TypeVar
from abc import ABC, abstractmethod

from ..bus.protocol import RegisterBus

R = TypeVar("R", bound="Register")


class Register(ABC):
    ADDRESS: ClassVar[int]
    WIDTH: ClassVar[int] = 1

    @abstractmethod
    def to_bytes(self) -> bytes: ...

    @classmethod
    @abstractmethod
    def from_bytes(cls: type[R], data: bytes) -> R: ...

    @classmethod
    def from_byte(cls: type[R], value: int) -> R:
        raise NotImplementedError

    @classmethod
    def read(cls: type[R], bus: RegisterBus, addr: int) -> R:
        data = bus.read(addr, cls.ADDRESS, cls.WIDTH)
        return cls.from_bytes(data)

    def write(self, bus: RegisterBus, addr: int) -> None:
        bus.write(addr, self.ADDRESS, self.to_bytes())

    @classmethod
    def _assert_data_width(cls: type[R], data: bytes) -> None:
        if len(data) != cls.WIDTH:
            raise ValueError(
                f"{cls.__name__} expects {cls.WIDTH} bytes, got {len(data)}"
            )
