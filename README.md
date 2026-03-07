# typed-registers

**typed-registers** is a small, type-safe library for working with hardware registers in Python.

It provides a simple abstraction for defining registers as Python classes and reading/writing them through a pluggable bus interface.

The goal is to make device register access:

* **typed**
* **explicit**
* **reusable**
* **testable**

instead of manually handling raw byte buffers.

This is especially useful when working with:

* I²C devices
* SPI devices
* embedded sensors
* ADCs / DACs
* microcontroller peripherals
* device drivers

# Features

* Typed register definitions using Python classes
* Clear separation between **register definitions** and **transport buses**
* Works with **I²C, SPI, UART, mock buses, or custom transports**
* Built-in register helpers:

  * `ByteRegister`
  * `Int24Register`
  * `Int32Register`
* Optional **SMBus / smbus2** support
* Fully typed (`Typing :: Typed`)
* Python 3.11+

# Installation

### Basic installation

```bash
pip install typed-registers
```

### With I²C support

```bash
pip install typed-registers[i2c]
```

This installs:

```
smbus2
```

# Quick Example

Define a register:

```python
from typed_registers import Int32Register


class TemperatureRegister(Int32Register):
    ADDRESS = 0x10
```

Read it from a device:

```python
from smbus2 import SMBus
from typed_registers.bus import SMBusRegisterBus

bus = SMBusRegisterBus(SMBus(1))

temp = TemperatureRegister.read(bus, addr=0x40)

print(temp.value)
```

Write a register:

```python
TemperatureRegister(value=42).write(bus, addr=0x40)
```

# Byte Registers

`ByteRegister` is useful for registers that represent a single byte with custom encoding.

Example:

```python
from typed_registers import ByteRegister


class ModeRegister(ByteRegister):
    ADDRESS = 0x01

    def __init__(self, enabled: bool):
        self.enabled = enabled

    def to_byte(self) -> int:
        return 0x01 if self.enabled else 0x00

    @classmethod
    def from_byte(cls, value: int):
        return cls(enabled=bool(value & 0x01))
```

# Built-in Register Types

The library provides a few common register types:

| Class           | Description           |
| --------------- | --------------------- |
| `ByteRegister`  | single byte register  |
| `Int24Register` | signed 24-bit integer |
| `Int32Register` | signed 32-bit integer |

All registers:

* validate byte width
* convert between Python values and raw bytes
* support `.read()` and `.write()` operations

# Bus Abstraction

Registers operate through the `RegisterBus` protocol:

```python
class RegisterBus(Protocol):
    def read(self, addr: int, reg: int, length: int) -> bytes
    def write(self, addr: int, reg: int, data: bytes) -> None
```

This allows registers to work with **any transport layer**.

For example:

* I²C
* SPI
* UART
* USB
* mock testing buses

# SMBus / I²C Support

If the `i2c` extra is installed, an SMBus adapter is available.

```python
from smbus2 import SMBus
from typed_registers.bus import SMBusRegisterBus

bus = SMBusRegisterBus(SMBus(1))
```

This works with both:

* `smbus`
* `smbus2`

# Testing

Because the bus is abstracted behind a protocol, it is easy to create test buses.

Example:

```python
class FakeBus:
    def read(self, addr, reg, length):
        return b"\x00\x00\x00\x2A"

    def write(self, addr, reg, data):
        print("write:", addr, reg, data)
```

Now registers can be tested without real hardware.

# Design Goals

This library aims to provide:

* **minimal API surface**
* **strong typing**
* **clear register semantics**
* **easy device driver construction**

without introducing heavy frameworks or complex abstractions.

# Status

This project is currently **alpha**.

The API may change while the design stabilizes.

# License

MIT License

# Author

Joshua B. Bussdieker

GitHub:
[https://github.com/jbussdieker](https://github.com/jbussdieker)
