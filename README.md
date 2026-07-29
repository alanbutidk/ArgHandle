# ArgHandle v2.1.0

A simple, lightweight alternative to `argparse`. No confusion, no boilerplate, just clean argument handling for your CLI tools.

Built because `argparse` is overkill for most scripts. ArgHandle gives you exactly what you need: register args, match them, print help/version, done.

## Installation

```
pip install arghandle==2.1.0
```

## Quick Start

```python
from arghandle import ArgHandle

cli = ArgHandle("YourProgramName", "v0.0.0") # Replace v0.0.0 with program version
# cli.ProgramName("mytool") <- This replaces the program name to mytool
# cli.Version("v1.0.0") <- This replaces the version number to v1.0.0
# cli.CustomVersionMsg("mytool, custom message") <- Overrides the --version/-v output entirely

cli.RegisterArg(["--output", "-o"], StrictIndex=1, StrictIndex_ExitOnError=True, HelpMsg="Output file")
cli.RegisterArg(["--input", "-i"], VarIndex=2, HelpMsg="Input file")

cli.PrintOnNoArgs("No arguments provided. Use --help or -h for usage.")
cli.HandleBasic()

if cli.IsArgInActualArgs("--input") or cli.IsArgInActualArgs("-i"):
    print(f"Input: {cli.input}")
```

Running `mytool --help` prints:

```
mytool v0.0.0 --help called:
  [--help, -h]: Print this help message and exit.
  [--output, -o]: Output file
  [--input, -i]: Input file
```

Running `mytool --version` prints:

```
mytool v0.0.0
```

## API

### `ArgHandle(ProgramName: str, Version: str)`

Main class. Instantiate once at the start of your program.

```python
cli = ArgHandle("mytool", "v1.0.0")
```

---

### `ProgramName(String: str)`

Sets the program name shown in help/version output.

```python
cli.ProgramName("mytool")
```

---

### `Version(String: str)`

Sets the version string shown in help/version output.

```python
cli.Version("v1.0.0")
```

---

### `CustomVersionMsg(Msg: str)`

Overrides the default `--version`/`-v` output with a custom message.

```python
cli.CustomVersionMsg("mytool, built by you")
```

---

### `RegisterArg(Flags, StrictIndex=None, StrictIndex_ExitOnError=False, VarIndex=None, *, HelpMsg)`

Registers an argument to the help screen, and optionally enforces a strict position in `sys.argv` or injects a `sys.argv` value directly onto the instance.

- `Flags`: list of flags/commands (e.g. `["--output", "-o"]`)
- `StrictIndex`: if set, the arg must appear at this index in `sys.argv`
- `StrictIndex_ExitOnError`: if `True`, exits with an error when the arg is at the wrong index; if `False`, returns `StrictIndexBroken`
- `VarIndex`: if set, sets an attribute on the instance (named after the first flag, e.g. `--output` becomes `cli.output`) to the value of `sys.argv[VarIndex]`
- `HelpMsg`: description shown in help output

```python
cli.RegisterArg(["--output", "-o"], StrictIndex=1, StrictIndex_ExitOnError=True, HelpMsg="Output file")
cli.RegisterArg(["--input", "-i"], VarIndex=2, HelpMsg="Input file")

print(cli.input)  # value of sys.argv[2], or NoVarIndex() if out of range
```

**Returns:**

| Return Type         | Meaning                                                        |
| ------------------- | --------------------------------------------------------------- |
| `Registered`        | Successfully registered                                        |
| `NotRegistered`     | Empty or invalid flags list                                    |
| `NoKwargs`          | No `HelpMsg` provided                                          |
| `OverlimitKwargs`   | More than one kwarg passed                                     |
| `StrictIndexBroken` | Arg not at required index and `StrictIndex_ExitOnError=False`  |

---

### `HandleBasic(Exit=True)`

Checks args for `--version`/`-v` first, then `--help`/`-h`, printing the corresponding output. Exits after either by default. If neither is present, does nothing.

```python
cli.HandleBasic()
```

Version output (or the message set via `CustomVersionMsg`, if any):

```
mytool v1.0.0
```

Help output:

```
mytool v1.0.0 --help called:
  [--help, -h]: Print this help message and exit.
  [--output, -o]: Output file
```

---

### `PrintOnNoArgs(String, NoColor=False, Warn=False, Exit=True)`

Prints a message if no arguments are passed (`sys.argv` has fewer than 2 entries). Exits by default.

- `NoColor`: disables ANSI color codes
- `Warn`: uses yellow instead of red when `NoColor` is `False`
- `Exit`: raises `SystemExit` if `True`, otherwise just prints

```python
cli.PrintOnNoArgs("No arguments provided.", Exit=True)
```

---

### `IsArgInActualArgs(String) -> bool`

Returns `True` if the string is present anywhere in `sys.argv`.

```python
if cli.IsArgInActualArgs("--output"):
    ...
```

---

### `IsArgMatch(String, AtIndex) -> bool`

Returns `True` if the string matches the arg at a specific index in `sys.argv`.

```python
if cli.IsArgMatch("--output", 1):
    ...
```

---

### `ErrorArgPrint(Text: str, Warn=False, Exit=True)`

Prints an error (red by default, yellow if `Warn=True`) and exits by default.

```python
cli.ErrorArgPrint("Argument not recognized, use --help/-h for usage!")
```

---

### `SetVariableToIndex(VarName, Index) -> str | IndexOutOfRange`

Sets an attribute on the instance (named `VarName`) to the value of `sys.argv` at the given index, and returns that value. Returns `IndexOutOfRange` if the index doesn't exist.

```python
output = cli.SetVariableToIndex("MyOutput", 2)
if isinstance(output, IndexOutOfRange):
    raise SystemExit("No value provided at index 2\n")
print(output)        # "myfile.c"
print(cli.MyOutput)  # also "myfile.c"
```

---

### `WhereArg(Arg: str) -> int | ArgNotFound`

Returns the index in `sys.argv` where a substring match for `Arg` is found, or `ArgNotFound` if it isn't present.

```python
idx = cli.WhereArg("--output")
if isinstance(idx, ArgNotFound):
    print("not provided")
```

---

### `NextAfter(InitVar) -> str | NotFoundInArgs`

Given a value previously set via a `VarIndex`-registered arg (or a raw string present in `sys.argv`), returns the `sys.argv` value immediately after it. Returns `NotFoundInArgs` if there's nothing after it, or if `InitVar` is itself a `NoVarIndex`/`NotFoundInArgs` sentinel.

```python
cli.RegisterArg(["--input", "-i"], VarIndex=2, HelpMsg="Input file")
following = cli.NextAfter(cli.input)
```

---

### `ArgCount() -> int`

Returns the total number of arguments including the script name.

```python
print(cli.ArgCount())
```

---

## Return Types

All return type classes are importable directly:

```python
from arghandle import (
    Registered,
    NotRegistered,
    NoKwargs,
    OverlimitKwargs,
    StrictIndexBroken,
    IndexOutOfRange,
    NoVarIndex,
    ArgNotFound,
    NotFoundInArgs,
)
```

| Return Type          | Meaning                                                               |
| --------------------- | ------------------------------------------------------------------------ |
| `Registered`          | Returned when an argument is successfully registered                     |
| `NotRegistered`       | Returned when the argument list is empty or invalid                      |
| `NoKwargs`            | Returned when no `HelpMsg` kwarg is provided                             |
| `OverlimitKwargs`     | Returned when more than one kwarg is provided                            |
| `StrictIndexBroken`   | Returned when an arg isn't at the required `StrictIndex`                 |
| `IndexOutOfRange`     | Returned when the specified index is out of range from `sys.argv`        |
| `NoVarIndex`          | Returned when `VarIndex` is out of range from `sys.argv`                 |
| `ArgNotFound`         | Returned when `WhereArg` can't find the argument                         |
| `NotFoundInArgs`      | Returned when `NextAfter` couldn't find the value                        |

---

## Legacy

ArgHandle also ships a pure-Python `Legacy` class - the original implementation, kept for backwards compatibility. It does not use `setattr`-based attribute injection, has no `VarIndex`/`NextAfter` support, uses `HandleHelp` (not `HandleBasic`) with no version support, and is deprecated in favor of the main `ArgHandle` class. A `DeprecationWarning` is raised on instantiation.

```python
from arghandle import Legacy

cli = Legacy()
cli.RegisterArg(["--output", "-o"], HelpMsg="Output file")
cli.HandleHelp()
```

`Legacy` defines its own copies of the sentinel return types (`Registered`, `NotRegistered`, `NoKwargs`, `OverlimitKwargs`, `StrictIndexBroken`, `IndexOutOfRange`, `NoVarIndex`, `ArgNotFound`, `NotFoundInArgs`) in `arghandle.legacy_arghandle` - these are **not** the same classes as the ones exported from the top-level `arghandle` package, so `isinstance()` checks against `Legacy`'s results must use the legacy versions:

```python
from arghandle.legacy_arghandle import NotRegistered as LegacyNotRegistered

result = cli.RegisterArg([], HelpMsg="test")
isinstance(result, LegacyNotRegistered)  # True
```

`Legacy` supports: `ProgramName`, `ArgCount`, `PrintOnNoArgs`, `IsArgMatch`, `IsArgInActualArgs`, `RegisterArg`, `HandleHelp`, `SetVariableToIndex` (static, returns the value only - no attribute injection), and `WhereArg`.

New projects should use `ArgHandle`, not `Legacy`.

---

## Real World Example

ArgHandle was built as part of [AutoBuild](https://github.com/alanbutidk/AutoBuild), a Make-like build system with its own `.abuild` syntax. Check it out to see ArgHandle in action in a real project.

## License

GPLv3, see [LICENSE](https://github.com/alanbutidk/ArgHandle/blob/main/LICENSE) for details.