import json
import subprocess
from pathlib import Path
from wt_settings.core.models import Settings

_KNOWN_PACKAGES = [
    "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
    "Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe",
]

def _discover_via_powershell(pkg: str) -> Path | None:
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", "[Environment]::GetFolderPath('LocalApplicationData')"],
            capture_output=True, text=True, timeout=5,
        )
        if win_path := result.stdout.strip():
            result2 = subprocess.run(["wslpath", win_path], capture_output=True, text=True, timeout=5)
            if wsl_path := result2.stdout.strip():
                path = Path(wsl_path) / "Packages" / pkg / "LocalState" / "settings.json"
                return path if path.exists() else None
    except Exception:
        pass
    return None

def _discover_via_glob(pkg: str) -> Path | None:
    matches = sorted(Path("/mnt/c/Users").glob(f"*/AppData/Local/Packages/{pkg}/LocalState/settings.json"))
    return matches[0] if matches else None

def discover_settings_path() -> Path:
    """Auto-discover the Windows Terminal settings.json path."""
    for pkg in _KNOWN_PACKAGES:
        if path := _discover_via_powershell(pkg):
            return path
        if path := _discover_via_glob(pkg):
            return path
    raise FileNotFoundError("Could not find Windows Terminal settings.json.")

def load_settings(path: Path) -> Settings:
    with open(path, "r", encoding="utf-8-sig") as f:
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
