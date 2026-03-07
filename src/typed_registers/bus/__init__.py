from .protocol import RegisterBus

__all__ = ["RegisterBus"]

try:
    from .smbus import SMBusRegisterBus

    __all__.append("SMBusRegisterBus")
except ImportError:
    pass
