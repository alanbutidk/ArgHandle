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

# Before HelpMsg, it can take StrictIndex=[INT] & StrictIndex_ExitOnError=[True/False]

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
from typing import Union

# import warnings
# import os
# import re
# import textwrap

# Enable VT100 on Windows if detected platform is win32
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


class ArgNotFound:
    """Returned when WhereArg cannot find the argument from self.args (sys.argv[1:])"""

    pass


class ArgValue:
    """Auto-set on self by RegisterArg for a present flag. Truthy like True (so
    `if cli.output:` still works), but also carries .value so it can return whatever is there.
    the flag in sys.argv, or None if the flag was passed bare / nothing followed it.
    Usage: if cli.output: print(f"Output: {cli.output.value}")"""

    def __init__(self, Value: str | None):
        self.value = Value

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"ArgValue({self.value!r})"


class NotFoundInArgs:
    """Returned when ArgHandle.NextAfter couldnt find the value."""

    pass


# End of returnable Classes


# Start of ArgHandle
class ArgHandle:
    """ArgHandle() is the main class of arghandle.
    It has these functions:

    R: Returns <TYPE>

    - ProgramName(string: str), R: None
    - Version(string: str), R: None
    - CustomVersionMsg(string: str), R: None
    - ArgCount(), R: int()
    - PrintOnNoArgs(text: str, NoColor: bool=False, Warn: bool=False, Exit: bool=True), R: None
    --------------
    - SetVariableToIndex(VariableName: str, Index: int), R: str() OR IndexOutOfRange()
    - IsArgMatch(Arg: str, Index: int), R: True/False
    --------------
    - IsArgInActualArgs(Arg: str), R: bool;True/False
    - ErrorArgPrint(text: str, Warn: bool=False, Exit: bool=True)
    --------------
    - RegisterArg(Flags: list, StrictIndex: int=None, StrictIndex_ExitOnError: bool=False, HelpMsg: str=\"\")
        RegisterArg(...), R: Registered() OR NotRegistered() OR OverlimitKwargs() OR NoKwargs() OR StrictIndexBroken()
        Also auto-sets an attribute on self (argparse style) named after Flags[0], ArgValue()/False.

    - RegisterArgs(ArgDefs: list[dict]), R: list of whatever RegisterArg() returns per dict
        Takes same arguments as RegisterArg but at a 'bulk-level', meaning you can register many arguments without calling RegisterArg many times.

    --------------
    - HandleBasic(), R: None
    - Parse(Exit: bool=True), R: None
        Combines HandleBasic and PrintOnNoArgs to reduce boilerplate.

    - WhereArg(Arg: str), R: ArgNotFound() OR int()
    - NextAfter(Arg: str), R: NotFoundInArgs() OR str()

    """

    def __init__(self, ProgramName: str, Version: str, NoArgsMsg: str | None = None):
        # NoArgsMsg: Lets you skip PrintOnNoArgs at class initliazation.
        self.args = (
            sys.argv
        )  # 0: Script Name, 1: --help/-h OR --version/-v OR --AnyOtherArg
        self._CustomVersionMsg = False
        self._ProgramName = ProgramName
        self._Version = Version
        self._NoArgsMsg = NoArgsMsg
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
        **kwargs,
    ) -> Union[Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken]:
        """Register a argument so arghandle knows how to work with it.

        Usage:
            cli = ArgHandle(\"Program\", \"v1.0.0\")

        cli.RegisterArg(["--output", "-o"], StrictIndex=1, StrictIndex_ExitOnError=True, HelpMsg="Output file")
        print(cli.output)

        kwargs:
            HelpMsg="Description shown in help"

        Automatically sets an attribute on self (argparse style, via setattr) named after
        Flags[0] stripped of leading dashes, e.g. ["--banner", "-b"] -> self.banner.
        If the flag was present in sys.argv, the attribute is an ArgValue() (truthy, and
        carries .value = whatever came right after the flag, or None if nothing did).
        If the flag was NOT present, the attribute is plain False.
        Use hasattr()/getattr() on the instance if you need to check this dynamically.

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

        _, HelpMsg = next(iter(kwargs.items()))
        Name = Flags[0].lstrip("-").replace("-", "_")
        self._ArgsRegistered[Name] = {"Flags": Flags, "HelpMsg": HelpMsg}

        MatchedFlag = next((Flag for Flag in Flags if Flag in self.args), None)
        if MatchedFlag is not None:
            FlagIdx = self.args.index(MatchedFlag)
            NextIdx = FlagIdx + 1
            FollowingValue = self.args[NextIdx] if NextIdx < len(self.args) else None
            setattr(self, Name, ArgValue(FollowingValue))
        else:
            setattr(self, Name, False)

        return Registered()

    def RegisterArgs(
        self, ArgDefs: list
    ) -> list[
        Union[Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken]
    ]:
        """Bulk-register multiple arguments in one call instead of one RegisterArg() call
        per flag. Added v2.6.0 purely to cut boilerplate, internally this just loops and
        calls RegisterArg() for each dict, so behavior/return-types per-arg are identical.

        Usage:
            cli.RegisterArgs([
                {"Flags": ["--output", "-o"], "HelpMsg": "Output file"},
                {"Flags": ["--banner", "-b"], "HelpMsg": "Runs banner"},
            ])

        Each dict's keys map directly to RegisterArg()'s params: "Flags" (required),
        "StrictIndex", "StrictIndex_ExitOnError", and "HelpMsg" (goes through as the
        HelpMsg kwarg).

        Returns:
            A list of whatever RegisterArg() returned for each dict, in the same order.
        """
        Results = []
        for ArgDef in ArgDefs:
            ArgDef = dict(ArgDef)
            Flags = ArgDef.pop("Flags", [])
            StrictIndex = ArgDef.pop("StrictIndex", None)
            StrictIndex_ExitOnError = ArgDef.pop("StrictIndex_ExitOnError", False)
            Results.append(
                self.RegisterArg(
                    Flags,
                    StrictIndex=StrictIndex,
                    StrictIndex_ExitOnError=StrictIndex_ExitOnError,
                    **ArgDef,
                )
            )
        return Results

    def HandleBasic(self, Exit=True):
        if len(self.args) <= 1:
            return
        FirstArg = self.args[1]

        if FirstArg in ("--version", "-v"):
            if not self._CustomVersionMsg:
                print(
                    f"\033[36m{self._ProgramName}\033[0m \033[33m{self._Version}\033[0m"
                )
            else:
                print(f"{self._CustomVersionMsg}")

            if Exit:
                raise SystemExit
        if FirstArg in ("--help", "-h"):
            CalledArg = next(
                (Arg for Arg in self.args if Arg in ["--help", "-h"]), self.args[0]
            )

            print(f"{self._ProgramName} {self._Version} {CalledArg} called:")

            for _, Info in self._ArgsRegistered.items():
                Flags = ", ".join(Info["Flags"])
                Msg = Info["HelpMsg"]
                print(f"\033[36m  [{Flags}]\033[0m: \033[33m{Msg}\033[0m")

            if Exit:
                raise SystemExit

    def Parse(self, Exit=True):
        """Boilerplate reducing function to handle HandleBasic and PrintOnNoArgs. Recommend read the DOCS.md at https://github.com/alanbutidk/arghandle for more info."""
        if self._NoArgsMsg is not None:
            self.PrintOnNoArgs(self._NoArgsMsg)
        self.HandleBasic(Exit=Exit)

    def WhereArg(self, Arg: str) -> Union[int, ArgNotFound]:
        for i in range(len(self.args)):
            if Arg in self.args[i]:
                return i
        return ArgNotFound()

    def NextAfter(self, InitVar) -> Union[str, NotFoundInArgs]:
        if isinstance(InitVar, str) and InitVar in self.args:
            ArgIdx = self.args.index(InitVar)
            NextIdx = ArgIdx + 1
            if NextIdx < len(self.args):
                return self.args[NextIdx]
            return NotFoundInArgs()

        return NotFoundInArgs()


# End of ArgHandle class


def Main() -> None:
    print("Here is 'arghandle' as ASCII Blocks :)")
    print("""\033[36m █████  ██████   ██████  ██   ██  █████  ███    ██ ██████  ██      ███████ 
██   ██ ██   ██ ██       ██   ██ ██   ██ ████   ██ ██   ██ ██      ██      
███████ ██████  ██   ███ ███████ ███████ ██ ██  ██ ██   ██ ██      █████   
██   ██ ██   ██ ██    ██ ██   ██ ██   ██ ██  ██ ██ ██   ██ ██      ██      
██   ██ ██   ██  ██████  ██   ██ ██   ██ ██   ████ ██████  ███████ ███████ 

v2.6.0\033[0m					 """)


# End of text banner


def Cli():
    cli = ArgHandle("ArgHandle", "v2.6.0")
    cli.RegisterArg(["--banner", "-b"], HelpMsg="Runs the Main() function")
    cli.PrintOnNoArgs("No arguments given! Use --help/-h for usage.")
    cli.HandleBasic()
    if cli.banner:  # pyright: ignore
        Main()
        raise SystemExit  # Again so we cant pass after this
    else:
        cli.ErrorArgPrint("Argument not recognized, use --help/-h for usage!")


if __name__ == "__main__":
    Cli()
