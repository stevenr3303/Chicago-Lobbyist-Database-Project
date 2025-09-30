# Chicago Lobbyist Database Application

A small Python application that reads from `Chicago_Lobbyists.db` and displays lobbyist information. The project includes a simple CLI and a Tkinter GUI frontend. The GUI captures and displays output that previously was printed to the console, and provides a friendlier user interface for the same commands.

## Features
- Browse the database for lobbyists by name (supports SQL wildcards _ and %)
- View full lobbyist details (address, years registered, employers, total compensation)
- Show top-N lobbyists for a given year (by total compensation) and their clients
- Register an existing lobbyist for a new year
- Set or update a lobbyist's salutation
- GUI with toolbar, status bar, save-output, and redirected stdout/stderr so existing prints appear in the GUI

## Requirements
- Python 3.8+ (tested with Python 3.11)
- Standard library modules used: `sqlite3`, `tkinter`, `logging`
- No 3rd-party packages required

Note: On Windows, `tkinter` is included with the standard Python installer. If you used a minimal distribution, install the OS package that provides tkinter.

## Files of interest
- `gui_main.py` — the Tkinter GUI entrypoint (recommended)
- `main.py` — legacy CLI code (if you prefer the terminal)
- `objecttier.py` — builds objects from the database results
- `datatier.py` — executes SQL against the SQLite DB (uses logging for errors)
- `Chicago_Lobbyists.db` — the SQLite database file the app connects to (must be in the same folder or update the path in the code)

## Quick start (Windows PowerShell)

Run the GUI (recommended):

```powershell
python .\gui_main.py
```

Run the CLI (if you want the original interactive prompt):

```powershell
python .\main.py
```

## GUI usage
- Use the toolbar buttons to run the same operations as the CLI:
  - General Stats, Find Lobbyists, Lobbyist Details, Top N, Register Year, Set Salutation
- Output appears in the scrollable text area. Use File → Save Output or the Save Output button (or Ctrl+S) to save the current output to a text file.
- Use Exit or Ctrl+Q to quit (stdout/stderr and DB connections are cleaned up on exit).

## Notes about logging and prints
- `datatier.py` uses `logging.error(...)` for SQL or DB errors. The GUI redirects `sys.stdout` and `sys.stderr` into the GUI output area, so both prints and logged errors should be visible there.
- If you prefer to capture everything into a file automatically, consider using Python's `logging` module with a `FileHandler` or adding `sys.stdout` redirection at the launcher level.

## Troubleshooting
- "Unable to open database": make sure `Chicago_Lobbyists.db` exists in the project folder or adjust the path in `gui_main.py` / `main.py` when connecting with `sqlite3.connect('<path>')`.
- GUI doesn't appear / tkinter error: ensure Python installation includes tkinter and you launched with the correct interpreter.
- If a command raises an error, check the GUI output for logged error messages; those come from `datatier.py` and are intended to help diagnose SQL issues.


