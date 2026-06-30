# ArgHandle

A simple, lightweight alternative to `argparse`. No confusion, no boilerplate, just clean argument handling for your CLI tools.

Built because `argparse` is overkill for most scripts. ArgHandle gives you exactly what you need: register args, match them, print help, done.

## Installation

```
pip install arghandle
```

## Quick Start

```python
from arghandle import ArgHandle

cli = ArgHandle()
cli.ProgramName("mytool")

cli.RegisterArg(["--version", "-v"], HelpMsg="Prints the version and exit")
cli.RegisterArg(["build"], HelpMsg="Build the project")
cli.RegisterArg(["--output", "-o"], StrictIndex=2, StrictIndex_ExitOnError=True, HelpMsg="Output file")

cli.PrintOnNoArgs("No arguments provided. Use --help or -h for usage.", Exit=True)
cli.HandleHelp()

if cli.IsArgInActualArgs("--version") or cli.IsArgInActualArgs("-v"):
    raise SystemExit("mytool v1.3.3\n")

if cli.IsArgInActualArgs("build"):
    output = cli.SetVariableToIndex(2)
    print(f"Building: {output}")
```

Running `mytool --help` prints:

```
mytool --help/-h called:
  [--help, -h]: Prints this help message and exit
  [--version, -v]: Prints the version and exit
  [build]: Build the project
  [--output, -o]: Output file

```

## API

### `ArgHandle()`

Main class. Instantiate once at the start of your program.

```python
cli = ArgHandle()
```

---

### `ProgramName(String: str)`

Sets the program name shown in the help header.

```python
cli.ProgramName("mytool")
```

---

### `RegisterArg(Flags, StrictIndex=None, StrictIndex_ExitOnError=False, VarIndex=None, *, HelpMsg)`

Registers an argument to the help screen, and optionally enforces a strict position in `sys.argv` or injects an `sys.argv` value directly onto the instance.

- `Flags`: list of flags/commands (e.g. `["--version", "-v"]`)
- `StrictIndex`: if set, the arg must appear at this index in `sys.argv`
- `StrictIndex_ExitOnError`: if `True`, exits with an error when the arg is at the wrong index; if `False`, returns `StrictIndexBroken`
- `VarIndex`: if set, sets an attribute on the instance (named after the first flag, e.g. `--output` becomes `cli.output`) to the value of `sys.argv[VarIndex]`
- `HelpMsg`: description shown in help output

```python
cli.RegisterArg(["--version", "-v"], HelpMsg="Prints the version and exit")
cli.RegisterArg(["--output", "-o"], StrictIndex=2, StrictIndex_ExitOnError=True, HelpMsg="Output file")
cli.RegisterArg(["--input", "-i"], VarIndex=2, HelpMsg="Input file")

print(cli.input)  # value of sys.argv[2], or NoVarIndex() if out of range
```

**Returns:**

| Return Type         | Meaning                                                       |
| ------------------- | ------------------------------------------------------------- |
| `Registered`        | Successfully registered                                       |
| `NotRegistered`     | Empty or invalid flags list                                   |
| `NoKwargs`          | No `HelpMsg` provided                                         |
| `OverlimitKwargs`   | More than one kwarg passed                                    |
| `StrictIndexBroken` | Arg not at required index and `StrictIndex_ExitOnError=False` |

---

### `HandleHelp(Exit=True)`

Checks if `--help` or `-h` is in args and prints the help screen. Exits by default.

```python
cli.HandleHelp()
```

Output format:

```
mytool --help/-h called:
  [--help, -h]: Prints this help message and exit
  [--version, -v]: Prints the version and exit

```

---

### `PrintOnNoArgs(String, Exit=False)`

Prints a message if no arguments are passed. Optionally exits.

```python
cli.PrintOnNoArgs("No arguments provided.", Exit=True)
```

---

### `IsArgInActualArgs(String) -> bool`

Returns `True` if the string is present anywhere in `sys.argv[1:]`.

```python
if cli.IsArgInActualArgs("build"):
    ...
```

---

### `IsArgMatch(String, AtIndex) -> bool`

Returns `True` if the string matches the arg at a specific index in `sys.argv[1:]`.

```python
if cli.IsArgMatch("build", 0):
    ...
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

Returns the index in `self.args` (`sys.argv[1:]`) where a substring match for `Arg` is found, or `ArgNotFound` if it isn't present.

```python
idx = cli.WhereArg("--output")
if isinstance(idx, ArgNotFound):
    print("not provided")
```

---

### `NextAfter(InitVar) -> str | NotFoundInArgs`

Given a value previously set via a `VarIndex`-registered arg, returns the `sys.argv` value immediately after it. Returns `NotFoundInArgs` if there's nothing after it, or if `InitVar` is itself a `NoVarIndex`/`NotFoundInArgs` sentinel.

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

| Return Type         | Meaning                                                              |
| -------------------- | --------------------------------------------------------------------- |
| `Registered`         | Returned when an argument is successfully registered                  |
| `NotRegistered`      | Returned when the argument list is empty or invalid                   |
| `NoKwargs`           | Returned when no `HelpMsg` kwarg is provided                          |
| `OverlimitKwargs`    | Returned when more than one kwarg is provided                         |
| `StrictIndexBroken`  | Returned when an arg isn't at the required `StrictIndex`               |
| `IndexOutOfRange`    | Returned when the specified index is out of range from `sys.argv`     |
| `NoVarIndex`         | Returned when `VarIndex` is out of range from `sys.argv`               |
| `ArgNotFound`        | Returned when `WhereArg` can't find the argument                      |
| `NotFoundInArgs`     | Returned when `NextAfter` couldn't find the value                     |

---

## Legacy

ArgHandle also ships a pure-Python `Legacy` class - the original implementation, kept for backwards compatibility. It does not use `setattr`-based attribute injection, has no `VarIndex`/`NextAfter` support, and is deprecated in favor of the main `ArgHandle` class. A `DeprecationWarning` is raised on instantiation.

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