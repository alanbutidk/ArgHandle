"""ArgHandle is a library made to simplify using arguments with a ALMOST Pure-Python implementation."""

import sys
from typing import Union
import warnings

# Read tutorial at end of file.


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
    def __init__(self):
        self.args = sys.argv[1:]
        self._ProgramName = "PROGRAM"
        self._ArgsRegistered = {
            "Help": {
                "Flags": ["--help", "-h"],
                "HelpMsg": "Print this help message and exit.",
            }
        }

    def ProgramName(self, String: str):
        self._ProgramName = String

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
        print(f"{self._ProgramName} --help/-h called:")
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
        return NotFoundInArgs()


# End of ArgHandle

"""Tutorial on arghandle:

ArgHandle is a library made to simplify using sys.argv[]
This is a tutorial on how to use it...

So for example if our function, test() takes 2 variables. x and y...
We can directly take them from the sys.argv. So heres how to do it.

!THIS PART ENDS HERE, AFTER THE FUNCTION IS WHEN THE CODE STARTS!"""


def Main():
    print("This test is to showcase ArgHandle, and the logic behind this is simple.")
    print("""\033[34m █████  ██████   ██████  ██   ██  █████  ███    ██ ██████  ██      ███████ 
██   ██ ██   ██ ██       ██   ██ ██   ██ ████   ██ ██   ██ ██      ██      
███████ ██████  ██   ███ ███████ ███████ ██ ██  ██ ██   ██ ██      █████   
██   ██ ██   ██ ██    ██ ██   ██ ██   ██ ██  ██ ██ ██   ██ ██      ██      
██   ██ ██   ██  ██████  ██   ██ ██   ██ ██   ████ ██████  ███████ ███████                                                           
\033[0mv1.3.2                    """)


# End of cool thing

"""Now, our function is ready, so we shall use it...
It takes None (I am NONE) <- Arguments. and returns arghandle as ascii block art+The version of arghandle.
So we start our handler...
"""

if __name__ == "__main__":
    import subprocess

    subprocess.run(
        "", shell=True
    )  # This enables color code support (or colors the terminal.)
    cli = ArgHandle()
    cli.RegisterArg(["--test", "-t"], HelpMsg="Runs the Main() function")
    cli.RegisterArg(["--version", "-v"], HelpMsg="Prints version and exits")
    if cli.IsArgInActualArgs("-h") or cli.IsArgInActualArgs("--help"):
        cli.HandleHelp()
        raise SystemExit  # Just so we cant pass after this
    if cli.IsArgInActualArgs("--test") or cli.IsArgInActualArgs("-t"):
        Main()
        raise SystemExit  # Again so we cant pass after this
    if cli.IsArgInActualArgs("--version") or cli.IsArgInActualArgs("-v"):
        print("ArgHandle v1.3.2")
        raise SystemExit  # So we cant pass after this.

"""Now, we instantiated the class like: cli = ArgHandle().
BUT, Now which functions do we get as not instantiated ones.

We get these ones: SetVariableToIndex(), ArgCount(), PrintOnNoArgs(
The order of using the functions are simple, you instantiate a variable,
Register a argument using RegisterArg(["--MyFlag", "--MyFlag2"], and a optional HelpMsg="Help Message here"
and then you can call functions like IsArgInActualArgs to check if the flags are called.
and call HandleHelp() if --help/-h is called.

ArgHandle usage:
    cli = ArgHandle()
    cli.RegisterArg(["--output", "-o"], StrictIndex=2, StrictIndex_ExitOnError=True, HelpMsg="Output file")
    if isinstance(cli.output, NoVarIndex):
        raise SystemExit("No output file provided\n")
    print(cli.output)
"""
