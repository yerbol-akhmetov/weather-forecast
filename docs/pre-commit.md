<!--
SPDX-FileCopyrightText:  Weather-Forecast authors

SPDX-License-Identifier: CC-BY-4.0
-->

# Pre-commit checks

[pre-commit](https://pre-commit.com/) runs automatic checks before each commit. If a hook fails, the commit is blocked until the issue is fixed.

## Install

From the project root, with the virtual environment activated:

```bash
pip install -r requirements.txt
pre-commit install
```

Run this once after cloning the repository. Your friend should do the same.

## What gets checked

| Hook | What it does |
|---|---|
| `check-merge-conflict` | Blocks commits that still contain merge conflict markers |
| `end-of-file-fixer` | Ensures files end with a single newline |
| `mixed-line-ending` | Normalizes line endings (LF/CRLF) |
| `trailing-whitespace` | Removes trailing spaces at line ends |
| `check-added-large-files` | Blocks files larger than 2 MB |
| `ruff` | Lints Python code (imports, unused variables, common bugs) and auto-fixes some issues |
| `ruff-format` | Formats Python code to a consistent style |
| `yamllint` | Checks YAML syntax and style in config files |

Configuration files:

- [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) — which hooks run
- [`pyproject.toml`](../pyproject.toml) — Ruff lint and format rules
- [`.yamllint`](../.yamllint) — YAML lint rules

## Run manually

Check all files without committing:

```bash
pre-commit run --all-files
```

Check only staged files:

```bash
pre-commit run
```

## How it works on commit

1. You run `git commit`
2. pre-commit runs the hooks on staged files
3. If a hook modifies files (for example Ruff formatting), those changes are written to disk
4. You stage the updated files and commit again
5. If a hook reports an error you must fix yourself, fix it and retry the commit

## Skip hooks (use sparingly)

```bash
git commit --no-verify
```

Only use this when you have a good reason. Do not skip hooks routinely.
