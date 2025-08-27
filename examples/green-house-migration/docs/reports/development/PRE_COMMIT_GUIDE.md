# Pre-commit Configuration Guide

## Overview

This project uses pre-commit hooks to automatically enforce code quality
standards and formatting before each commit. This ensures consistent code style
and catches common issues early.

## What Pre-commit Does

### 🔧 **Python Code Quality**

#### Black (Code Formatter)

- **Purpose:** Automatically formats Python code to a consistent style

- **What it fixes:**

  - Line length (79 characters)
  - Indentation
  - Import formatting
  - Code spacing

- **Command:** `black --line-length=79`

#### isort (Import Sorter)

- **Purpose:** Organizes and sorts Python imports

- **What it fixes:**

  - Groups imports (standard library, third-party, local)
  - Sorts imports alphabetically
  - Removes duplicate imports

- **Command:** `isort --profile=black --line-length=79`

#### flake8 (Linter)

- **Purpose:** Checks for code style and potential errors

- **What it checks:**

  - Line length violations
  - Unused imports
  - Undefined variables
  - Code complexity
  - Style violations

- **Ignored rules:** `B008,E501,W293,F401,F841,E402,W503`

- **Command:** `flake8 --max-line-length=79 --max-complexity=15`

#### mypy (Type Checker)

- **Purpose:** Static type checking for Python

- **What it checks:**

  - Type annotations
  - Type consistency
  - Import errors

- **Configuration:** `--ignore-missing-imports --no-strict-optional`

### 📝 **Documentation & Files**

#### Prettier (Formatter)

- **Purpose:** Formats various file types consistently

- **Supported files:**

- **YAML:** `.yml`, `.yaml` files

- **JSON:** `.json` files

- **Markdown:** `.md` files

- **What it fixes:**
  - Consistent indentation
  - Line endings
  - Spacing
  - Quote style

#### Trailing Whitespace

- **Purpose:** Removes trailing spaces and tabs

- **What it fixes:**
  - Lines ending with spaces
  - Inconsistent whitespace
  - Clean file endings

#### End of File Fixer

- **Purpose:** Ensures files end with a newline

- **What it fixes:**
  - Files without final newline
  - Consistent file endings

### 🔍 **Quality Checks**

#### YAML/JSON Validation

- **Purpose:** Validates YAML and JSON syntax

- **What it checks:**
  - Valid YAML structure
  - Valid JSON format
  - Syntax errors

#### Large Files Check

- **Purpose:** Prevents accidentally committing large files

- **What it checks:**
  - Files larger than 500KB
  - Binary files
  - Generated files

#### Merge Conflicts

- **Purpose:** Detects unresolved merge conflicts

- **What it checks:**
  - `<<<<<<<`, `=======`, `>>>>>>>` markers
  - Incomplete merges

#### Debug Statements

- **Purpose:** Prevents debug code from being committed

- **What it checks:**
  - `pdb.set_trace()`
  - `breakpoint()`
  - `import pdb`

#### Case Conflicts

- **Purpose:** Detects filename case conflicts

- **What it checks:**
  - Files with same name but different case
  - Cross-platform compatibility issues

#### Docstring First

- **Purpose:** Ensures docstrings come before code

- **What it checks:**
  - Module-level docstrings
  - Function docstrings placement

#### Private Key Detection

- **Purpose:** Prevents accidental commit of private keys

- **What it checks:**
  - Private key patterns
  - API keys
  - Secrets

### 📝 **Commit Message Formatting**

#### Commitizen

- **Purpose:** Enforces conventional commit message format

- **Format:** `type(scope): description`

- **Examples:**
  - `feat(api): add new endpoint for candidates`
  - `fix(dashboard): resolve chart display issue`
  - `docs(readme): update installation instructions`

## How to Use

### Installation

```bash
# Install pre-commit
pipenv install pre-commit --dev

# Install git hooks
pipenv run pre-commit install
```

### Manual Execution

```bash
# Run on all files
pipenv run pre-commit run --all-files

# Run on specific files
pipenv run pre-commit run --files path/to/file.py

# Run specific hook
pipenv run pre-commit run black --all-files
```

### Automatic Execution

- Pre-commit runs automatically on every `git commit`

- If any hook fails, the commit is blocked

- Fixed files are automatically staged

- You can commit again after fixes are applied

## Configuration Details

### Current Settings

#### Black Configuration

```yaml
args: [--line-length=79]
```

#### isort Configuration

```yaml
args: [--profile=black, --line-length=79]
```

#### flake8 Configuration

```yaml
args:
  [
    --max-line-length=79,
    --max-complexity=15,
    --ignore=B008,
    E501,
    W293,
    F401,
    F841,
    E402,
    W503,
  ]
```

#### mypy Configuration

```yaml
args: [--ignore-missing-imports, --no-strict-optional]
additional_dependencies: [types-requests]
```

### Ignored Flake8 Rules

- **B008:** Function calls in argument defaults

- **E501:** Line too long

- **W293:** Blank line contains whitespace

- **F401:** Unused imports

- **F841:** Unused variables

- **E402:** Module level import not at top of file

- **W503:** Line break before binary operator

## Benefits

### For Developers

1. **Consistent Code Style:** All code follows the same formatting rules

2. **Early Error Detection:** Catches issues before they reach the repository

3. **Automated Fixes:** Many issues are automatically corrected

4. **Reduced Review Time:** Less time spent on formatting discussions

### For the Project

1. **Code Quality:** Maintains high code quality standards

2. **Consistency:** Ensures all contributors follow the same standards

3. **Documentation:** Keeps documentation properly formatted

4. **Security:** Prevents accidental commit of sensitive information

## Troubleshooting

### Common Issues

#### Hook Fails on Commit

```bash
# The hook will show what needs to be fixed
# Fix the issues and commit again
git add .
git commit -m "your message"
```

#### Pre-commit Not Running

```bash
# Reinstall hooks
pipenv run pre-commit install

# Check if hooks are installed
ls -la .git/hooks/
```

#### Specific Hook Issues

```bash
# Run specific hook to see detailed output
pipenv run pre-commit run flake8 --all-files
```

### Bypassing Pre-commit (Not Recommended)

```bash
# Only use in emergencies
git commit --no-verify -m "emergency fix"
```

## Customization

### Adding New Hooks

Edit `.pre-commit-config.yaml` and add new hooks:

```yaml
- repo: https://github.com/example/hook-repo
  rev: v1.0.0
  hooks:
    - id: hook-name
      args: [--config=.hook-config]
```

### Modifying Existing Hooks

Update the configuration in `.pre-commit-config.yaml`:

```yaml
- id: black
  args: [--line-length=88] # Change line length
```

### Local Configuration

Create `.pre-commit-config.local.yaml` for local-only hooks:

```yaml
repos:
  - repo: local
    hooks:
      - id: custom-hook
        name: Custom Hook
        entry: python scripts/custom_hook.py
        language: python
        files: \.py$
```

## Best Practices

1. **Always Run Pre-commit:** Let it run on every commit

2. **Fix Issues Promptly:** Address any failures immediately

3. **Keep Configuration Updated:** Update hook versions regularly

4. **Document Changes:** Update this guide when modifying configuration

5. **Team Communication:** Ensure all team members understand the setup

---

**Last Updated:** 2024-01-15
**Configuration Version:** 1.0.0
**Pre-commit Version:** 4.5.0
