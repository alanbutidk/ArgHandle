"""ArgHandle is a library made to simplify using arguments.
Read tutorial at end of APIs
"""

import sys
from typing import Union

# Custom return type classes
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
# End of Custom Classes

# Start of ArgHandle
class ArgHandle:
    def __init__(self):
        self.args = sys.argv[1:]
        self._ProgramName = "PROGRAM"
        self._ArgsRegistered = {
            "help": {
                "Flags": ["--help", "-h"],
                "HelpMsg": "Prints this help message and exit"
            }
        }

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

    def RegisterArg(self, Flags: list, StrictIndex: int = None, StrictIndex_ExitOnError: bool = False, **kwargs) -> Union[Registered, NotRegistered, NoKwargs, OverlimitKwargs, StrictIndexBroken, IndexOutOfRange]:
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

        # Check StrictIndex
        if StrictIndex is not None:
            matched = any(
                self.IsArgMatch(flag, StrictIndex - 1)
                for flag in Flags
            )
            if not matched and any(self.IsArgInActualArgs(flag) for flag in Flags):
                if StrictIndex_ExitOnError:
                    flag_str = ", ".join(Flags)
                    raise SystemExit(f"[{flag_str}] is not at index [{StrictIndex}]\n")
                else:
                    return StrictIndexBroken()

        _, HelpMsg = next(iter(kwargs.items()))
        Name = Flags[0].lstrip("-")
        self._ArgsRegistered[Name] = {
            "Flags": Flags,
            "HelpMsg": HelpMsg
        }
        return Registered()
    def RegisterToHelp(self, *args, **kwargs):
        raise DeprecationWarning("RegisterToHelp is now deprecated, use RegisterArg() instead [CHANGED FROM v1.1.0]")
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
    def SetVariableToIndex(Index: str) -> Union[str, IndexOutOfRange]:
        """Sets a variable to a specfic index.
        Usage: output = ArgHandle.SetVariableToIndex(2)
        If sys.argv[2] holds \"myfile.c\" then it will return myfile.c
        else it will return IndexOutOfRange"""
        
        if Index < len(sys.argv):
            return sys.argv[Index]
        return IndexOutOfRange()
# End of ArgHandle

"""Tutorial on arghandle:
ArgHandle is a library made to simplify using sys.argv[]
This is a tutorial on how to use it...

So for example if our function, test() takes 2 variables. x and y...
We can directly take them from the sys.argv. So heres how to do it.

!THIS PART ENDS HERE, AFTER THE FUNCTION IS WHEN THE CODE STARTS!"""
def test(x: int, y: bool) -> tuple | bool:
    if x == 1 and y:
        return True
    elif x == 1 and not y:
        return False
    else:
        return False
    print("Hey! This function, test() ran because you directly called python on me (with the --test/-t flag)...")

"""Now, our function is ready, so we shall use it...
It takes a integer, then a boolean. If the int is 1 and y is True.
Then it returns True
if x is 1 but y is False, it returns False. else False as well....
So we start our handler..."""
if __name__ == "__main__":
    cli = ArgHandle()
    cli.RegisterArg(["--test", "-t"], HelpMsg="Runs the test() function")
    if cli.IsArgInActualArgs("--help") or cli.IsArgInActualArgs("-h"):
        cli.HandleHelp()
    if cli.IsArgInActualArgs("--test") or cli.IsArgInActualArgs("-t"):
        test()
"""Now, we instantiated the class like: cli = ArgHandle().
BUT, Now which functions do we get as not instantiated ones.

We get these ones: SetVariableToIndex(), ArgCount(), PrintOnNoArgs().

The order of using the functions are simple, you instantiate a variable,
Register a argument using RegisterArg([\"--MyFlag\", \"--MyFlag2\"], and a optional HelpMsg=\"Help Message here\"
and then you can call functions like IsArgInActualArgs to check if the flags are called.
and call HandleHelp() if --help/-h is called.
"""
