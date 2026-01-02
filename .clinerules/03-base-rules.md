# Base Execution Rules (Always-On)

## Python Execution Policy
- **Default:** Do not run ad-hoc Python via command line (`python -c ...` or inline heredocs).
- **Instead:** Create a temp script in `Scripts/Tmp/YY_MM_DD_HHMM-SS.py` and execute it immediately.
  - Example filename: `26_01_02_1121-36.py`
  - Script should contain full logic (imports, arguments, output capture).
  - This keeps code auditable and reproducible.

## Terminal Commands in Python Scripts
- When Python scripts need to run terminal commands (via `subprocess` or similar):
  - Include a user approval prompt at script start (once per script run).
  - If `sudo` is required, prompt user for password input within the script, then use it for the command.

## Exceptions
- Purely read-only shell commands (e.g., `ls`, `cat`, `grep`) may still be run directly if trivial.
- File I/O and terminal scripts from Python are encouraged.
