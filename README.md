# MyPythonModule

[![Build Status](https://travis-ci.com/yourusername/MyPythonModule.svg?branch=main)](https://travis-ci.com/yourusername/MyPythonModule)
[![Coverage Status](https://coveralls.io/repos/github/yourusername/MyPythonModule/badge.svg?branch=main)](https://coveralls.io/github/yourusername/MyPythonModule?branch=main)
[![PyPI version](https://badge.fury.io/py/MyPythonModule.svg)](https://badge.fury.io/py/MyPythonModule)

An object-oriented wrapper for the KIPR Botball library with additional functionalities. 

## Installation

The module is installed using pip:

```bash
pip install IHSBotballKit
```
## Usage

Documentation can be found in the source code or stubs. Examples use cases are provided in the examples folder. 

## Contributing

Contributions are welcome! Please follow the following style guides:
* Use standard python syntax and naming conventions(e.g. snake_case for variables, CamelCase for classes).
* 
* All importable members must be documented using [Google style docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
* Type hinting is not required but strongly recommended whenever possible.
* It is recommended to use a static type checker such as [mypy](https://mypy.readthedocs.io/en/stable/) while contributing to the package.
* Create stubs in the stubs folder after you've made all the changes. A good way to do that is to use [mypy's stubgen](https://mypy.readthedocs.io/en/stable/stubgen.html).
    ```bash
    # generate all the stubs at once
    stubgen -p ./IHSBotballKit -v --include-docstrings -o ./stubs
    # generate stubs for one (or more) file
    stubgen ./IHSBotballKit/file.py ./IHSBotballKit/file2.py -v --include-docstrings -0 ./stubs
    ```
    * note: the stubs generated will have some issues and incomplete typing. It is your job to fix them before committing the code.

## Acknowledgements

* [Botballkit](https://pypi.org/project/BotballKit/) - For inspiration and some functionality.
## Issues

If you encounter any issues, please create a new issue here. Please be detailed in the description of the issue, include relevant background information (e.g. operating system, software versions), expected behavior, and how to reproduce the issue.