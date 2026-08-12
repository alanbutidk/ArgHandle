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

from .oindex_arghandle import OIndex_ArgHandle

__all__ = [
    "ArgHandle",
    "OIndex_ArgHandle",
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
