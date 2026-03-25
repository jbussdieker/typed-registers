# typed-registers

**typed-registers** is a small, type-safe library for working with hardware registers in Python.

It lets you define registers as Python classes and interact with them through a pluggable bus interface — eliminating manual byte manipulation while keeping full control over hardware behavior.

The goal is to make register access:

* **typed**
* **explicit**
* **composable**
* **testable**

instead of opaque byte slicing and bit masking.

## Features

* Typed register definitions using Python classes
* Clear separation between **register logic** and **transport**
* Works with **I²C, SPI, UART, mock buses, or custom transports**
* Minimal API surface
* Fully typed (`Typing :: Typed`)
* Python 3.11+

### Built-in Register Types

| Class           | Description                           |
| --------------- | ------------------------------------- |
| `ByteRegister`  | single byte register                  |
| `Int24Register` | signed 24-bit integer                 |
| `Int32Register` | signed 32-bit integer                 |
| `BlockRegister` | structured multi-byte register blocks |

## Installation

```bash
pip install typed-registers
```

With I²C support:

```bash
pip install typed-registers[i2c]
```

## Quick Example

```python
from typed_registers import Int32Register

class TemperatureRegister(Int32Register):
    ADDRESS = 0x10
```

```python
from smbus2 import SMBus
from typed_registers.bus import SMBusRegisterBus

bus = SMBusRegisterBus(SMBus(1))

temp = TemperatureRegister.read(bus, addr=0x40)
print(temp.value)
```

## Byte Registers

```python
from dataclasses import dataclass
from typed_registers import ByteRegister

@dataclass(slots=True, frozen=True)
class ModeRegister(ByteRegister):
    ADDRESS = 0x01

    enabled: bool

    def to_byte(self) -> int:
        return 0x01 if self.enabled else 0x00

    @classmethod
    def from_byte(cls, value: int):
        return cls(enabled=bool(value & 0x01))
```

## Block Registers

`BlockRegister` is used for structured multi-byte registers.

You define how raw bytes map into fields:

```python
from dataclasses import dataclass
from typed_registers import BlockRegister

@dataclass(slots=True, frozen=True)
class ExampleBlock(BlockRegister):
    ADDRESS = 0x20
    WIDTH = 3

    high: int
    low: int

    @classmethod
    def _decode(cls, data: bytes):
        return cls(
            high=data[0],
            low=(data[1] << 8) | data[2],
        )
```

Read it like any other register:

```python
value = ExampleBlock.read(bus, addr=0x40)
```

By default, `BlockRegister` is read-only. Override `_encode()` to support writing.

## Bus Abstraction

Registers operate through the `RegisterBus` protocol:

```python
class RegisterBus(Protocol):
    def read(self, addr: int, reg: int, length: int) -> bytes
    def write(self, addr: int, reg: int, data: bytes) -> None
```

This allows registers to work with any transport layer.

## SMBus / I²C Support

```python
from smbus2 import SMBus
from typed_registers.bus import SMBusRegisterBus

bus = SMBusRegisterBus(SMBus(1))
```

Supports both `smbus` and `smbus2`.

## Testing

Because the bus is abstracted, registers are easy to test:

```python
class FakeBus:
    def read(self, addr, reg, length):
        return b"\x00\x00\x00\x2A"

    def write(self, addr, reg, data):
        print("write:", addr, reg, data)
```

## Design Philosophy

This library intentionally keeps things simple:

* Registers are **first-class objects**
* Encoding/decoding is **explicit and local**
* No hidden magic or frameworks
* Hardware behavior remains visible

The register map *is the API*.

## Status

**Alpha**

The API is stabilizing and already used in real drivers, but may evolve.

## License

MIT License

## Author

**Joshua B. Bussdieker**
[https://github.com/jbussdieker](https://github.com/jbussdieker)
