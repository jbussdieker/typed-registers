from typing import Protocol

from .protocol import RegisterBus


class _SMBusLike(Protocol):
    def read_byte_data(self, addr: int, reg: int) -> int: ...
    def write_byte_data(self, addr: int, reg: int, value: int) -> None: ...
    def read_i2c_block_data(self, addr: int, reg: int, length: int) -> list[int]: ...
    def write_i2c_block_data(self, addr: int, reg: int, data: list[int]) -> None: ...


class SMBusRegisterBus(RegisterBus):

    def __init__(self, bus: _SMBusLike) -> None:
        self.bus = bus

    def read(self, addr: int, reg: int, length: int) -> bytes:
        if length == 1:
            return bytes([self.bus.read_byte_data(addr, reg)])

        data = self.bus.read_i2c_block_data(addr, reg, length)
        return bytes(data)

    def write(self, addr: int, reg: int, data: bytes) -> None:
        if len(data) == 1:
            self.bus.write_byte_data(addr, reg, data[0])
        else:
            self.bus.write_i2c_block_data(addr, reg, list(data))
