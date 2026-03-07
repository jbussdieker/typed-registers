from typing import Protocol, runtime_checkable


@runtime_checkable
class RegisterBus(Protocol):
    def read(self, addr: int, reg: int, length: int) -> bytes: ...
    def write(self, addr: int, reg: int, data: bytes) -> None: ...
