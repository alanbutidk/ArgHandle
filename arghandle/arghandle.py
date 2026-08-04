"""
ArgHandle is a library made to simplify using arguments with a ALMOST Pure-Python implementation.
This version of arghandle uses sys.argv[0] instead of starting with [1].

This is a simple tutorial on ArgHandle:

The main arghandle class is ArgHandle()
It takes these arguments:

- ProgramName (Arg1)
- ProgramVersion (Arg2)

So it would look like: ArgHandle(\"MyProgram\", \"v1.0.0\")

A simple code example for ArgHandle is:

cli = ArgHandle(\"Program\", \"v1.0.0\")
cli.PrintOnNoArgs(\"No arguments supplied!\")
cli.RegisterArg([\"-a1\", \"--arg1\"], HelpMsg=\"This is argument 1\")

# Before HelpMsg, it can take StrictIndex=\[INT\] & StrictIndex_ExitOnError=\[True/False\]

cli.HandleBasic()

# Now we can check if a1 was there:

if cli.a1:
    # LOGIC (I am going to print hello, world)
    print(\"Hello, World!\")
    raise SystemExit
else:
    cli.ErrorArgPrint(\"Unknown argument supplied! Use --help/-h for usage.\")

For now, this is ArgHandle, read the docs at the github repository.
"""

# Imports:
import sys
from typing import Tuple, Union
import warnings
# import os
# import re
# import textwrap

# Read tutorial at end of file.

if sys.platform == "win32":
    import ctypes

    STD_OUTPUT_HANDLE = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    kernel32 = ctypes.windll.kernel32
    hOut = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    Mode = ctypes.c_ulong()

    kernel32.GetConsoleMode(hOut, ctypes.byref(Mode))
    kernel32.SetConsoleMode(hOut, Mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)


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
class ArgHandle:
    def __init__(self, ProgramName: str, Version: str):
        self.args = sys.argv
        self._CustomVersionMsg = False
        self._ProgramName = ProgramName
        self._Version = Version
        self._ArgsRegistered = {
            "Help": {
                "Flags": ["--help", "-h"],
                "HelpMsg": "Print this help message and exit.",
            }
        }

    def ProgramName(self, String: str):
        self._ProgramName = String

    def Version(self, String: str):
        self._Version = String

    def CustomVersionMsg(self, Msg: str):
        self._CustomVersionMsg = Msg

    def ArgCount(self) -> int:
        return len(sys.argv)

    def PrintOnNoArgs(
        self, String: str, NoColor: bool = False, Warn: bool = False, Exit: bool = True
    ):
        if not NoColor and not Warn:
            CLR = "\033[31m"
            RST = "\033[0m"
        elif not NoColor and Warn:
            CLR = "\033[33m"
            RST = "\033[0m"
        else:
            CLR = ""
            RST = ""

        if len(sys.argv) < 2:
            if Exit:
                raise SystemExit(f"{CLR}{String}{RST}")
            print(f"{CLR}{String}{RST}")

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

    def ErrorArgPrint(
        self, Text: str, Warn: bool = False, Exit: bool = True
    ) -> tuple | None:
        COLOR = "\033[31m" if not Warn else "\033[33m"
        print(f"{COLOR}{Text}\033[0m")
        if Exit:
            raise SystemExit

    def RegisterArg(
        self,
        Flags: list,
        StrictIndex: int | None = None,
        StrictIndex_ExitOnError: bool | None = False,
        VarIndex: int | None = None,
        **kwargs,
    ) -> Union[Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken]:
        """Register a argument so arghandle knows how to work with it.

        Usage:
            cli = ArgHandle(\"Program\", \"v1.0.0\")

        cli.RegisterArg(["--output", "-o"], StrictIndex=1, StrictIndex_ExitOnError=True, HelpMsg="Output file")
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
            if 0 <= VarIndex < len(sys.argv):
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
            "RegisterToHelp is now deprecated, use ArgHandle().RegisterArg() instead [CHANGED FROM v1.1.0]",
            category=DeprecationWarning,
        )

    def HandleBasic(self, Exit=True):
        if any(Flag == Arg for Arg in self.args for Flag in ["--version", "-v"]):
            if not self._CustomVersionMsg:
                print(
                    f"\033[36m{self._ProgramName}\033[0m \033[33m{self._Version}\033[0m"
                )
            else:
                print(f"{self._CustomVersionMsg}")

            if Exit:
                raise SystemExit()
        if any(Flag == Arg for Arg in self.args for Flag in ["--help", "-h"]):
            CalledArg = next(
                (Arg for Arg in self.args if Arg in ["--help", "-h"]), self.args[0]
            )

            print(f"{self._ProgramName} {self._Version} {CalledArg} called:")

            for Name, Info in self._ArgsRegistered.items():
                Flags = ", ".join(Info["Flags"])
                Msg = Info["HelpMsg"]
                print(f"\033[36m  [{Flags}]\033[0m: \033[33m{Msg}\033[0m")

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


# End of ArgHandle class


def Main():
    print("This test is to showcase ArgHandle, and the logic behind this is simple.")
    print("""\033[36m █████	 ██████	  ██████  ██   ██  █████  ███	 ██ ██████	██		███████ 
██	 ██ ██	 ██ ██		 ██	  ██ ██	  ██ ████	██ ██	██ ██	   ██	   
███████ ██████	██	 ███ ███████ ███████ ██ ██	██ ██	██ ██	   █████   
██	 ██ ██	 ██ ██	  ██ ██	  ██ ██	  ██ ██	 ██ ██ ██	██ ██	   ██	   
██	 ██ ██	 ██	 ██████	 ██	  ██ ██	  ██ ██	  ████ ██████  ███████ ███████															 

v2.2.0\033[0m					 """)


# End of text banner


def Cli():
    cli = ArgHandle("ArgHandle", "v2.2.0")
    cli.RegisterArg(["--test", "-t"], HelpMsg="Runs the Main() function")
    cli.PrintOnNoArgs("No arguments given! Use --help/-h for usage.")
    cli.HandleBasic()
    if cli.test:
        Main()
        raise SystemExit  # Again so we cant pass after this
    else:
        cli.ErrorArgPrint("Argument not recognized, use --help/-h for usage!")


if __name__ == "__main__":
    Cli()
