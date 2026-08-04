# ArgHandle Documentation
**ArgHandle** is a library written with NO custom-depends except Python StdLib.

It offers great parsing features without the complex commands argparse introduces.

It is installable via pip with: `pip install arghandle`

## API

This is where the docs actually begin:

The class is called `ArgHandle()`, It holds the following functions:

- ProgramName() :: Use to change program name
- Version() :: Use to change Version
- CustomVersionMsg() :: Use to change the default version message to a custom one.

Brief info:

Intoduced in v2.1.0, They modify _Version, and _ProgramName (Version and ProgramName) in the class.
CustomVersionMsg() changes _CustomVersionMsg in the class.

- @staticmethod: ArgCount() :: Returns a integer the length of sys.argv
- @staticmethod: PrintOnNoArgs :: Print a message when no arguments are given

Arguments allowed:

PrintOnNoArgs(Msg, NoColor=False, Warn=False, Exit=True)

- NoColor removes the color \033[31m and \033[0m.
- Warn changes the color to \033[33m (or a yellow)
- Exit is defaulted to True, it exits the program after printing the message.


- SetVariableToIndex() :: Info below!!

SetVariableToIndex() takes 2 arguments:

- VariableName (str)
- Index (int)

It uses setattr to make a variable inside the initialized class of whatever name you place in it with the value of sys.argv[index]

If the index is out of range, the variable is set to: IndexOutOfRange()

- IsArgMatch(String: str, AtIndex: int) :: Checks if String is at sys.argv[AtIndex] with index out of range protection.
- IsArgInActualArgs(String: str) :: Runs a simple check if String is in sys.argv.
- ErrorArgPrint() :: Info below!!

ErrorArgPrint() takes many args, by default:
Text (str), it prints the Text as red unless Warn=True, and Exit=False only prints the text (doesn't exit).

- RegisterArg() :: Info below!!

RegisterArg() is the most complex function in ArgHandle, it can return many classes

The argument it takes are:

RegisterArg(Flags: list, StrictIndex=(int) (Not needed by default), StrictIndex_ExitOnError=False (Make it true to error if the index is broken), HelpMsg="Argument 1, Foo Bar.")

It takes the first item in the Flags list, and uses setattr to register it inside the initialized variable.

It strips - with _ (so --arg-1 becomes arg_1 in Python).

It can return:

- NotRegistered() (Returned if Flags is empty/False)
- NoKwargs() (Returned when you dont give a HelpMsg)
- OverlimitKwargs() (Returned when another kwargs is returned after HelpMsg)

- HandleBasic() :: Handles --help/-h and --version/-v
- WhereArg() :: Returns the index of the Arg asked for (Function arg: (str))

---

## Code example

```python
from arghandle import ArgHandle

cli = ArgHandle("Program", "v1.0.0")
cli.PrintOnNoArgs("No arguments given. Use --help/-h for usage.")
cli.RegisterArg(["--myarg1", "-ma1"], StrictIndex=1, StrictIndex_ExitOnError=True, HelpMsg="Returns the next string given after -ma1")
cli.HandleBasic()

if cli.myarg1:
  if cli.ArgCount() <= 2: 
    print(f"Next argument: {cli.NextAfter("--myarg1") or cli.NextAfter("-ma1")}")
  else:
    cli.ErrorArgPrint("Foo Bar...")
```

