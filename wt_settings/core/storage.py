import json
import os
import platform
import subprocess
from pathlib import Path
from wt_settings.core.models import Settings

_KNOWN_PACKAGES = [
    "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
    "Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe",
]

def discover_settings_path() -> Path:
    """Auto-discover the Windows Terminal settings.json path."""
    if platform.system() == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if not local_app_data:
            raise EnvironmentError("LOCALAPPDATA environment variable not found.")
        base = Path(local_app_data) / "Packages"
    else:
        result = subprocess.run(
            ["powershell.exe", "-Command", "[Environment]::GetFolderPath('LocalApplicationData')"],
            capture_output=True, text=True,
        )
        win_path = result.stdout.strip()
        if not win_path:
            raise EnvironmentError("Could not retrieve LOCALAPPDATA from Windows via PowerShell.")
        result2 = subprocess.run(["wslpath", win_path], capture_output=True, text=True)
        base = Path(result2.stdout.strip()) / "Packages"
    candidates = [base / pkg / "LocalState" / "settings.json" for pkg in _KNOWN_PACKAGES]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "Could not find Windows Terminal settings.json. Tried:\n"
        + "\n".join(str(p) for p in candidates)
    )

def load_settings(path: Path) -> Settings:
    with open(path, "r", encoding="utf-8") as f:
        return Settings.model_validate(json.load(f))

def save_settings(settings: Settings, path: Path, dry_run: bool = False) -> None:
    data = settings.model_dump(by_alias=True, exclude_none=True)
    if dry_run:
        print(f"[dry-run] Would write to {path}:")
        print(json.dumps(data, indent=4))
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"✓ Settings saved to {path}")
