# ArgHandle Documentation

ArgHandle is a small library for handling command line arguments in Python. It doesn't use any third party packages, just the standard library, so there's nothing extra to install besides ArgHandle itself.

The whole point of it is to be simpler than argparse. You don't have to learn a bunch of parser objects and subparsers, you just make one class, register your flags on it, and check if they were passed.

Install it with:

```
pip install arghandle
```

## Getting started

Everything starts with the ArgHandle class. You create one instance and give it your program's name and version:

```python
from arghandle import ArgHandle

cli = ArgHandle("MyProgram", "v1.0.0")
```

That's it, you now have a working cli object. From here you register the flags you care about and then check them.

## The ArgHandle class

When you create it, you give it:

* ProgramName (str), the name shown in help and version messages
* Version (str), the version shown in help and version messages
* NoArgsMsg (str, optional), a message to print automatically if the program was run with no arguments at all

That last one is optional, you can leave it out and handle the no args case yourself with PrintOnNoArgs if you want more control.

## Changing the name, version, and messages

Once the class exists you can still update these values later:

* `ProgramName("NewName")` changes the program name
* `Version("v2.0.0")` changes the version
* `CustomVersionMsg("some custom message")` replaces the built in version output with your own text. Pass `color=True` and it'll wrap it in cyan for you.
* `CustomHelpMsg("some custom message")` does the same thing but for the help output. Also takes `color=True`.

If you set a custom help message, ArgHandle stops building the automatic list of registered flags and just prints whatever you gave it instead.

## Checking argument count

`ArgCount()` just returns how many items are in sys.argv, nothing fancy, it's there so you don't have to import sys yourself if all you need is the count.

## Handling the no arguments case

`PrintOnNoArgs(text, NoColor=False, Warn=False, Exit=True)` checks if the program was run with no arguments (meaning sys.argv only has the script name in it) and if so, prints your message.

By default the message prints in red and the program exits right after. If you pass `Warn=True` instead it prints in yellow instead of red. If you pass `NoColor=True` it skips the color codes entirely, useful if you're piping output somewhere that doesn't render ANSI colors well. If you pass `Exit=False` it just prints the message and lets your program keep running instead of stopping it.

## Reading a specific argument by position

`SetVariableToIndex(VarName, Index)` grabs whatever is sitting at that index in sys.argv and stores it as an attribute on your cli object under the name you gave it.

So this:

```python
cli.SetVariableToIndex("MyFile", 2)
print(cli.MyFile)
```

will look at sys.argv[2] and set cli.MyFile to whatever string is there.

If that index doesn't exist (say your program was only run with one argument but you asked for index 2) it sets the attribute to an IndexOutOfRange object instead of crashing, and also returns that same object back to you so you can check it right away without needing to look at the attribute.

## Checking arguments manually

Two small helper methods if you want to check things yourself without registering anything:

* `IsArgMatch(String, AtIndex)` tells you if a specific string is sitting at a specific index in the arguments. Returns True or False, and it won't blow up if the index doesn't exist, it just returns False.
* `IsArgInActualArgs(String)` just checks if a string shows up anywhere at all in sys.argv, regardless of position. Also True or False.

## Printing errors

`ErrorArgPrint(Text, Warn=False, Exit=True)` prints your message in red by default (or yellow if Warn is True) and then exits the program unless you pass Exit=False.

This is meant for the case where the user passed something you don't recognize, so you can bail out cleanly with a readable message instead of a stack trace.

## Registering arguments

This is the main feature of the library so it deserves the most explanation.

`RegisterArg(Flags, StrictIndex=None, StrictIndex_ExitOnError=False, HelpMsg="")`

Flags is a list of strings, like `["--output", "-o"]`. The first item in that list becomes the name of an attribute that gets added to your cli object automatically, with the dashes stripped and any remaining dashes turned into underscores. So `--output` becomes `cli.output`, and something like `--my-flag` would become `cli.my_flag`.

After you call RegisterArg, that attribute will be set to one of two things:

* If the flag was present anywhere in sys.argv, the attribute becomes an ArgValue object. This object is truthy, so `if cli.output:` works exactly how you'd expect. It also carries whatever came right after the flag in sys.argv, which you get through `.value`, like `cli.output.value`. If nothing followed the flag, `.value` will just be None.
* If the flag was not present at all, the attribute is just plain False.

HelpMsg is required, it's the description that shows up when someone runs your program with --help. You always need to pass it as a keyword argument.

StrictIndex is optional and lets you require that a flag show up at an exact position in sys.argv (counting from 1, so the second overall argument would be StrictIndex=1). This is handy if your program expects a very specific argument order and you want to catch mistakes early. If the flag exists somewhere in the arguments but not at that exact index, and StrictIndex_ExitOnError is True, the program exits right there with an error. If StrictIndex_ExitOnError is left False, RegisterArg just returns a StrictIndexBroken object instead so you can handle it yourself.

RegisterArg can return one of these depending on what happened:

* Registered, everything went fine
* NotRegistered, you passed an empty Flags list
* NoKwargs, you forgot to pass HelpMsg
* OverlimitKwargs, you passed more than one keyword argument (only HelpMsg is allowed)
* StrictIndexBroken, explained above

## Registering a bunch of arguments at once

If you have a lot of flags, calling RegisterArg over and over gets repetitive. RegisterArgs (plural) lets you register many at once by passing a list of dictionaries:

```python
cli.RegisterArgs([
    {"Flags": ["--output", "-o"], "HelpMsg": "Output file"},
    {"Flags": ["--banner", "-b"], "HelpMsg": "Runs the banner"},
])
```

Each dictionary uses the same keys as RegisterArg's parameters. Behind the scenes this is really just a loop that calls RegisterArg once per dictionary, so the behavior and what gets returned for each one is identical to calling RegisterArg directly. You get back a list with one result per dictionary, in the same order you gave them.

## Built in help and version flags

`HandleBasic(Exit=True)` checks if the very first argument passed to your program was `--help`, `-h`, `--version`, or `-v`, and handles printing the right message and exiting if so.

For version, it prints your program name and version (or your CustomVersionMsg if you set one).

For help, it prints your program name, version, and then lists out every flag you've registered along with its HelpMsg, unless you've set a CustomHelpMsg, in which case it prints that instead.

## Cutting down on boilerplate

If you don't need fine control, `Parse(Exit=True)` bundles together PrintOnNoArgs (using the NoArgsMsg you gave when creating the class, if any) and HandleBasic, so you can skip calling both separately.

## Finding where an argument is

`WhereArg(Arg)` searches through sys.argv and gives you back the index of the first argument that contains the string you're looking for. Note that this checks if your string is contained inside each argument, not that it matches exactly, so searching for "out" would also match "--output". If nothing matches, it returns an ArgNotFound object.

## Getting the value right after a flag

`NextAfter(Arg)` looks for Arg somewhere in sys.argv and, if it finds it, returns whatever comes right after it. If the flag isn't found, or there's nothing after it in the list, you get back a NotFoundInArgs object instead of a string.

This is basically the same idea as the .value you get from ArgValue when you use RegisterArg, just usable without registering the flag first.

## A full example

```python
from arghandle import ArgHandle

cli = ArgHandle("Program", "v1.0.0")
cli.PrintOnNoArgs("No arguments given. Use --help or -h for usage.")
cli.RegisterArg(["--myarg1", "-ma1"], StrictIndex=1, StrictIndex_ExitOnError=True, HelpMsg="Returns the next value given after -ma1")
cli.HandleBasic()

if cli.myarg1:
    print(f"Next argument: {cli.myarg1.value}")
else:
    cli.ErrorArgPrint("Argument not recognized, use --help or -h for usage.")
```

Running this with `python program.py -ma1 hello` would set cli.myarg1 to an ArgValue with .value equal to "hello", and print "Next argument: hello".

## Quick reference

A short list of everything covered above, in case you just need a reminder of what's available:

* ProgramName, Version, CustomVersionMsg, CustomHelpMsg, change the basic info
* ArgCount, how many args were passed
* PrintOnNoArgs, print something and optionally exit if there were no args
* SetVariableToIndex, grab whatever is at a specific index
* IsArgMatch, IsArgInActualArgs, manual checks
* ErrorArgPrint, print an error and optionally exit
* RegisterArg, RegisterArgs, the main way to define flags
* HandleBasic, built in --help and --version support
* Parse, shortcut for PrintOnNoArgs plus HandleBasic
* WhereArg, find the index of an argument
* NextAfter, get the value that follows a given argument