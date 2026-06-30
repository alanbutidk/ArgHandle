"""LegacyArgHandle is the legacy version of arghandle. Made to simplify using arguments with a ALMOST Pure-Python implementation."""

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


# Start of Legacy class (Dont use it!)
class Legacy:
    def __init__(self):
        self.args = sys.argv[1:]  # list starting after <PROGRAM_SCRIPT_PATH>
        self._ProgramName = "PROGRAM"
        self._ArgsRegistered = {
            "help": {
                "Flags": ["--help", "-h"],
                "HelpMsg": "Prints this help message and exit",
            }
        }
        warnings.warn(
            "The old class 'ArgHandle' or now, Legacy is deprecated. \nPlease switch to the new ArgHandle class, Although you can still use the Legacy class.",
            category=DeprecationWarning,
            stacklevel=2,
        )

    def ProgramName(self, string: str):
        self._ProgramName = string

    @staticmethod
    def ArgCount() -> int:
        return len(sys.argv)

    @staticmethod
    def PrintOnNoArgs(string: str, Exit=False):
        if len(sys.argv) < 2:
            if Exit:
                raise SystemExit(f"{string}\n")
            print(f"{string}\n")

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
        **kwargs,
    ) -> Union[Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken]:
        """Registers an argument to the help screen and optionally enforces a strict index.

        Usage:
            cli.RegisterArg(["--version", "-v"], HelpMsg="Prints the version and exit")
            cli.RegisterArg(["--output", "-o"], StrictIndex=2, StrictIndex_ExitOnError=True, HelpMsg="Output file")

        kwargs:
            HelpMsg="Description shown in --help output"

        Returns:
            Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken

        Help format:
            [--version, -v]: Prints the version and exit
        """
        if not Flags or Flags == []:
            return NotRegistered()
        if not kwargs:
            return NoKwargs()
        if len(kwargs) > 1:
            return OverlimitKwargs()

        if StrictIndex is not None:
            matched = any(self.IsArgMatch(flag, StrictIndex - 1) for flag in Flags)
            if not matched and any(self.IsArgInActualArgs(flag) for flag in Flags):
                if StrictIndex_ExitOnError:
                    flag_str = ", ".join(Flags)
                    raise SystemExit(f"[{flag_str}] is not at index [{StrictIndex}]\n")
                else:
                    return StrictIndexBroken()

        _, HelpMsg = next(iter(kwargs.items()))
        Name = Flags[0].lstrip("-")
        self._ArgsRegistered[Name] = {"Flags": Flags, "HelpMsg": HelpMsg}
        return Registered()

    def RegisterToHelp(self, *args, **kwargs):
        raise DeprecationWarning(
            "RegisterToHelp is now deprecated, use RegisterArg() instead [CHANGED FROM v1.1.0]"
        )

    def HandleHelp(self, Exit=True):
        if not any(arg in self.args for arg in ["--help", "-h"]):
            return
        print(f"{self._ProgramName} --help/-h called:")
        for Name, Info in self._ArgsRegistered.items():
            Flags = ", ".join(Info["Flags"])
            Msg = Info["HelpMsg"]
            print(f"  [{Flags}]: {Msg}")
        if Exit:
            raise SystemExit()

    @staticmethod
    def SetVariableToIndex(Index: int) -> Union[str, IndexOutOfRange]:
        """Sets a variable to a specfic index.
        Usage: output = ArgHandle.SetVariableToIndex(2)
        If sys.argv[2] holds "myfile.c" then it will return myfile.c
        else it will return IndexOutOfRange"""

        if Index < len(sys.argv):
            return sys.argv[Index]
        return IndexOutOfRange()

    def WhereArg(self, Arg: str) -> str | Union[int, ArgNotFound]:
        for i in range(len(self.args)):
            if Arg in self.args[i]:
                return i
        return ArgNotFound()


# End of Legacy
