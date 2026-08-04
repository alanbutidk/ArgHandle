# pyright: ignore

from .arghandle import (
    ArgHandle,
    NotRegistered,
    Registered,
    NoKwargs,
    OverlimitKwargs,
    StrictIndexBroken,
    IndexOutOfRange,
    NoVarIndex,
    ArgNotFound,
    NotFoundInArgs,
)
from .legacy_arghandle import Legacy

from .oindex_arghandle import OIndexArgHandle

__all__ = [
    "ArgHandle",
    "OIndexArgHandle",
    "NotRegistered",
    "Registered",
    "NoKwargs",
    "OverlimitKwargs",
    "StrictIndexBroken",
    "IndexOutOfRange",
    "NoVarIndex",
    "ArgNotFound",
    "NotFoundInArgs",
    "Legacy",
]
