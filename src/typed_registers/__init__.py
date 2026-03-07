from .bus import RegisterBus
from .register import Register, ByteRegister, Int24Register, Int32Register

__all__ = [
    "RegisterBus",
    "Register",
    "ByteRegister",
    "Int24Register",
    "Int32Register",
]

try:
    from .bus import SMBusRegisterBus

    __all__.append("SMBusRegisterBus")
except ImportError:
    pass
