# ArgHandle

A simple, lightweight alternative to `argparse`. No confusion, no boilerplate, just clean argument handling for your CLI tools.

Built because `argparse` is overkill for most scripts. ArgHandle gives you exactly what you need: register args, match them, print help, done.

## Installation

```bash
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
    raise SystemExit("mytool v1.1.0\n")

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

### `ProgramName(string: str)`
Sets the program name shown in the help header.

```python
cli.ProgramName("mytool")
```

---

### `RegisterArg(Flags, StrictIndex=None, StrictIndex_ExitOnError=False, *, HelpMsg)`
Registers an argument to the help screen and optionally enforces a strict position in `sys.argv`.

- `Flags`: list of flags/commands (e.g. `["--version", "-v"]`)
- `StrictIndex`: if set, the arg must appear at this index in `sys.argv`
- `StrictIndex_ExitOnError`: if `True`, exits with an error when the arg is at the wrong index; if `False`, returns `StrictIndexBroken`
- `HelpMsg`: description shown in help output

```python
cli.RegisterArg(["--version", "-v"], HelpMsg="Prints the version and exit")
cli.RegisterArg(["--output", "-o"], StrictIndex=2, StrictIndex_ExitOnError=True, HelpMsg="Output file")
```

**Returns:**

| Return Type | Meaning |
|---|---|
| `Registered` | Successfully registered |
| `NotRegistered` | Empty or invalid flags list |
| `NoKwargs` | No `HelpMsg` provided |
| `OverlimitKwargs` | More than one kwarg passed |
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

### `PrintOnNoArgs(string, Exit=False)`
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

### `SetVariableToIndex(Index) -> str | IndexOutOfRange`
Returns the value of `sys.argv` at the given index. Returns `IndexOutOfRange` if the index doesn't exist.

```python
output = cli.SetVariableToIndex(2)
if isinstance(output, IndexOutOfRange):
    raise SystemExit("No value provided at index 2\n")
print(output)  # "myfile.c"
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
    IndexOutOfRange
)
```

---

## Real World Example

ArgHandle was built as part of [AutoBuild](https://github.com/alanbutidk/AutoBuild), a Make-like build system with its own `.abuild` syntax. Check it out to see ArgHandle in action in a real project.

## License

GPLv3, see [LICENSE](LICENSE) for details.