# PyLitarios - AI Coding Assistant Instructions

## Project Overview

PyLitarios is a collection of standalone Python utility scripts for Windows automation and productivity tasks. Each script is designed to be run independently or compiled to executables via PyInstaller.

## Architecture & Structure

- **No shared modules**: Each `.py` file is a self-contained script with its own main entry point
- **Single-file executables**: Scripts are designed to be packaged individually with `pyinstaller --onefile <script>.py`
- **Windows-specific**: Heavy use of `pywin32` for Windows service management and `tkinter` for GUI
- **Virtual environment**: `.venv/` directory contains isolated Python dependencies
- **Install dependencies**: Use `uv pip install -r requirements.txt` to install all required packages in the virtual environment

## Key Scripts & Patterns

### GUI Applications (Tkinter Pattern)

All GUI scripts follow this structure:
```python
import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        # Setup widgets and bindings
        
def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Examples**: `capture2base64.py`, `clicker.py`, `inicializaIIS.py`

### CLI Applications (argparse Pattern)

Command-line scripts use `sys.argv` parsing with detailed usage instructions:
```python
def print_usage():
    # Display comprehensive help text
    
def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)
    # Process commands
```

**Example**: `base64_converter.py` with `encode`/`decode` subcommands

### Windows Admin Privileges

Scripts requiring admin access (e.g., `inicializaIIS.py`) check privileges early:
```python
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
```

## Development Workflow

### Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Run scripts directly
python <script_name>.py
```

### Building Executables
```powershell
# Create standalone .exe
pyinstaller --onefile <script_name>.py
```

### Testing
- Manual testing only - no automated test framework
- Test with different screen resolutions for GUI scripts
- Test admin vs non-admin execution paths for IIS scripts

## Critical Conventions

1. **Error Handling**: Use `try/except` with `tkinter.messagebox.showerror()` for GUI feedback
2. **Threading**: Long-running GUI operations use `threading.Thread(daemon=True)` to prevent blocking
3. **User Feedback**: Rich visual feedback with emojis (📖, 🔄, 💾, ✅, ❌) in CLI outputs
4. **Encoding**: Always use UTF-8 encoding (`encoding='utf-8'`) for text file operations
5. **File Paths**: Use `Path` from `pathlib` or raw strings for Windows paths

## Dependencies & External Systems

- **pywin32**: Windows service management (`win32service`, `win32serviceutil`)
- **Pillow (PIL)**: Image capture and manipulation
- **pyperclip**: Clipboard operations for base64 strings
- **pyautogui**: Mouse automation
- **keyboard**: Global keyboard event monitoring

## Common Pitfalls

- GUI scripts must call `root.withdraw()` before screen capture to hide the window
- Service management requires administrator privileges - always check early
- Threading in Tkinter requires `.after()` for UI updates from background threads
- PyInstaller may need `--hidden-import` flags for dynamic imports (not currently needed)

## Code Style

- Function names: `snake_case`
- Class names: `PascalCase`
- Constants: `UPPER_CASE` (rarely used)
- GUI button text: Portuguese (target audience is Brazilian users)
- Comments and docstrings: English or Portuguese mixed

## When Adding New Scripts

1. Add script description to `README.md` under "Scripts Disponíveis" with emoji icon
2. Include comprehensive docstring at top of file
3. Add any new dependencies to `requirements.txt`
4. Test executable creation with PyInstaller
5. Document admin privilege requirements if applicable
