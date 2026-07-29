"""
OneIndexArgHandle is a library made to simplify using arguments with a ALMOST Pure-Python implementation.
This version of arghandle uses sys.argv[1:] instead of [0]
"""

import sys
from typing import Union
import warnings


# Start of returnable classes.
class NotRegistered:
    """Returned when the argument list is empty or invalid."""

    pass


class Registered:
    """Returned when the argument is successfully registered."""

    pass


class NoKwargs:
    """Returned when no HelpMsg kwarg is provided."""

    pass


class OverlimitKwargs:
    """Returned when more than one kwarg is provided."""

    pass


class StrictIndexBroken:
    """Returned when an arg is not at the required StrictIndex and StrictIndex_ExitOnError=False."""

    pass


class IndexOutOfRange:
    """Returned when the specific index is out of range from sys.argv."""

    pass


class NoVarIndex:
    """Returned when VarIndex is out of range from sys.argv."""

    pass


class ArgNotFound:
    """Returned when WhereArg cannot find the argument from self.args (sys.argv[1:])"""

    pass


class NotFoundInArgs:
    """Returned when ArgHandle.NextAfter couldnt find the value."""

    pass


# End of returnable Classes


# Start of ArgHandle
class OIndexArgHandle:
    def __init__(self, ProgramName: str, VersionName: str):
        self.args = sys.argv[1:]
        self._ProgramName = ProgramName
        self._VersionName = VersionName
        self._ArgsRegistered = {
            "Help": {
                "Flags": ["--help", "-h"],
                "HelpMsg": "Print this help message and exit.",
            }
        }

    def ProgramName(self, String: str):
        self._ProgramName = String
    
    def VersionName(self, String: str):
        self._VersionName = String

    @staticmethod
    def ArgCount() -> int:
        return len(sys.argv)

    @staticmethod
    def PrintOnNoArgs(String: str, Exit=False):
        if len(sys.argv) < 2:
            if Exit:
                raise SystemExit(f"{String}\n")
            print(f"{String}\n")

    def SetVariableToIndex(
        self, VarName: str, Index: int
    ) -> Union[str, IndexOutOfRange]:
        """Sets a variable to a specific index.
        Usage: Output = ArgHandle.SetVariableToIndex(\"YourVariableName\", 2), 2 is the index.
        If sys.argv[2] holds "myfile.c" then it will return myfile.c
        else it will return IndexOutOfRange"""

        if Index < len(sys.argv):
            setattr(self, VarName, sys.argv[Index])
            return sys.argv[Index]
        setattr(self, VarName, IndexOutOfRange())
        return IndexOutOfRange()

    def IsArgMatch(self, String: str, AtIndex: int) -> bool:
        if AtIndex < len(self.args):
            return self.args[AtIndex] == String
        return False

    def IsArgInActualArgs(self, String: str) -> bool:
        return String in self.args

    def RegisterArg(
        self,
        Flags: list,
        StrictIndex: int = None,
        StrictIndex_ExitOnError: bool = False,
        VarIndex: int = None,
        **kwargs,
    ) -> Union[Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken]:
        """RegisterArg with setattr variable injection.

        Usage:
            cli = ArgHandle()
            cli.RegisterArg(["--output", "-o"], StrictIndex=2, StrictIndex_ExitOnError=True, HelpMsg="Output file")
            print(cli.output)

        kwargs:
            HelpMsg="Description shown in help"

        Returns:
            Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken
        """
        if not Flags or Flags == []:
            return NotRegistered()
        if not kwargs:
            return NoKwargs()
        if len(kwargs) > 1:
            return OverlimitKwargs()

        if StrictIndex is not None:
            Matched = any(
                StrictIndex - 1 < len(self.args) and self.args[StrictIndex - 1] == Flag
                for Flag in Flags
            )
            if not Matched and any(Flag in self.args for Flag in Flags):
                if StrictIndex_ExitOnError:
                    FlagStr = ", ".join(Flags)
                    raise SystemExit(f"[{FlagStr}] is not at index [{StrictIndex}]\n")
                else:
                    return StrictIndexBroken()

        if VarIndex is not None:
            VarName = Flags[0].lstrip("-").replace("-", "_")
            if VarIndex < len(sys.argv):
                setattr(self, VarName, sys.argv[VarIndex])
            else:
                setattr(self, VarName, NoVarIndex())
            self._ArgsRegistered[VarName] = {
                "Flags": Flags,
                "HelpMsg": next(iter(kwargs.values())),
                "VarIndex": VarIndex,
            }

        _, HelpMsg = next(iter(kwargs.items()))
        Name = Flags[0].lstrip("-")
        self._ArgsRegistered[Name] = {"Flags": Flags, "HelpMsg": HelpMsg}
        return Registered()

    def RegisterToHelp(self, *Args, **Kwargs):
        warnings.warn(
            "RegisterToHelp is now deprecated, use RegisterArg() instead [CHANGED FROM v1.1.0]",
            category=DeprecationWarning,
        )

    def HandleHelp(self, Exit=True):
        if not any(Arg in self.args for Arg in ["--help", "-h"]):
            return
        print(f"{self._ProgramName} {self._VersionName} {self.args[0]} called:")
        for Name, Info in self._ArgsRegistered.items():
            Flags = ", ".join(Info["Flags"])
            Msg = Info["HelpMsg"]
            print(f"  [{Flags}]: {Msg}")
        if Exit:
            raise SystemExit()

    def WhereArg(self, Arg: str) -> Union[int, ArgNotFound]:
        for i in range(len(self.args)):
            if Arg in self.args[i]:
                return i
        return ArgNotFound()

    def NextAfter(self, InitVar) -> Union[str, NotFoundInArgs]:
        if isinstance(InitVar, (NoVarIndex, NotFoundInArgs)):
            return NotFoundInArgs()
        for Name, Info in self._ArgsRegistered.items():
            if (
                Info.get("VarIndex") is not None
                and getattr(self, Name, None) == InitVar
            ):
                NextIdx = Info["VarIndex"] + 1
                if NextIdx < len(sys.argv):
                    return sys.argv[NextIdx]
                return NotFoundInArgs()
        if isinstance(InitVar, str) and InitVar in self.args:
            ArgIdx = self.args.index(InitVar)
            NextIdx = ArgIdx + 1
            if NextIdx < len(self.args):
                return self.args[NextIdx]
            return NotFoundInArgs()
        return NotFoundInArgs()


# End of ArgHandle
