# ArgHandle v2.7.0

A simple, lightweight alternative to `argparse`. No confusion, no boilerplate, just clean argument handling for your CLI tools.

Built because `argparse` is overkill for most scripts. ArgHandle gives you exactly what you need: register args, match them, print help/version, done.

## Installation

```
pip install arghandle==2.7.0
```

## Quick Start

```python
from arghandle import ArgHandle

cli = ArgHandle("YourProgramName", "v0.0.0") # Replace v0.0.0 with program version
# cli.ProgramName("mytool") <- This replaces the program name to mytool
# cli.Version("v1.0.0") <- This replaces the version number to v1.0.0
# cli.CustomVersionMsg("mytool, custom message") <- Overrides the --version/-v output entirely

cli.RegisterArg(["--output", "-o"], StrictIndex=1, StrictIndex_ExitOnError=True, HelpMsg="Output file")
cli.RegisterArg(["--input", "-i"], HelpMsg="Input file")

cli.PrintOnNoArgs("No arguments provided. Use --help or -h for usage.")
cli.HandleBasic()

if cli.input:
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

## Documentation
**ArgHandle** documentation is availiable at [Documentation](https://github.com/alanbutidk/ArgHandle/blob/main/DOCS.md).

## Real World Example

ArgHandle was built as part of [AutoBuild](https://github.com/alanbutidk/AutoBuild), a Make-like build system with its own `.abuild` syntax. Check it out to see ArgHandle in action in a real project.

## License

GPLv3, see [LICENSE](https://github.com/alanbutidk/ArgHandle/blob/main/LICENSE) for details.
