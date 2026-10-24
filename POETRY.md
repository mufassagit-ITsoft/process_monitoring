# Poetry Setup

This project uses [Poetry](https://python-poetry.org/) to manage its Python environment. The program itself has no third-party dependencies (it uses only the Python standard library), so Poetry here mainly provides an isolated virtual environment and a pinned Python version.

## Requirements

- Python 3.9+ (3.6+ is enough for the program itself; recent Poetry releases need a newer Python)
- Poetry 2.x

## 1. Install Poetry

The recommended method is `pipx`:

```
sudo apt install pipx
pipx ensurepath
pipx install poetry
```

Restart the terminal, then confirm the install:

```
poetry --version
```

## 2. Set up the project

From the project folder (the one containing `main.py` and `process_rep.py`):

```
cd ~/Documents/Compfiles/ASU/IFT103_OS/Labs/process_reports
```

**If `pyproject.toml` already exists**, skip to step 3.

**If it does not**, create one:

```
poetry init
```

Answer the prompts, or press Enter to accept the defaults. Then make sure the file marks this as a script project rather than an installable package, with no dependencies required:

```toml
[project]
name = "process-reports"
version = "0.1.0"
description = "Cleans a raw top capture into a readable report"
requires-python = ">=3.9"
dependencies = []

[tool.poetry]
package-mode = false

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

`package-mode = false` tells Poetry not to try to install the project itself, which is correct because it is a set of scripts, not a package.

## 3. Create the environment

```
poetry install --no-root
```

This builds a virtual environment for the project. With no dependencies, it finishes quickly.

## 4. Run the program

Use `poetry run` so the program uses the project's environment:

```
poetry run python main.py process_moitoring.txt
poetry run python main.py process_moitoring.txt -o report.txt
poetry run python main.py --delete process_moitoring.txt -y
```

All the options in `README.md` work the same way after `poetry run python main.py`.

## Optional: activate the environment

To avoid typing `poetry run` each time, print the activation command and run it:

```
poetry env activate
```

Poetry prints a line such as `source /path/to/.venv/bin/activate`. Run that line, then use `python main.py ...` directly. Type `deactivate` to leave the environment.

## Useful commands

| Command | Purpose |
|---------|---------|
| `poetry env info` | Show the environment's Python version and location |
| `poetry env use python3.12` | Choose which Python the environment uses |
| `poetry add <package>` | Add a dependency (none are needed now) |
| `poetry show` | List installed packages |
| `poetry check` | Validate `pyproject.toml` |
| `poetry env remove --all` | Delete the environment so it can be rebuilt |

## Troubleshooting

- **`poetry: command not found`**: run `pipx ensurepath` and open a new terminal.
- **`The current project could not be installed`**: use `poetry install --no-root`, or add `package-mode = false` under `[tool.poetry]`.
- **Python version error**: the `requires-python` value in `pyproject.toml` must match an installed Python. Check with `python3 --version`, and change the value or use `poetry env use` with a suitable interpreter.
- **`ModuleNotFoundError: process_rep`**: run the command from the folder that contains `process_rep.py`, since `main.py` imports it from the same folder.