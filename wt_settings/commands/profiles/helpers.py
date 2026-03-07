import typer
from wt_settings.commands.profiles.models import Profile
from wt_settings.core.models import Settings

def find_profile(settings: Settings, name: str) -> tuple[Profile | None, int]:
    """Find a profile by name. Returns (profile, index) or (None, -1)."""
    for i, profile in enumerate((settings.profiles and settings.profiles.list) or []):
        if profile.name == name:
            return profile, i
    return None, -1

def get_profile_or_abort(settings: Settings, name: str) -> tuple[Profile, int]:
    """Find a profile by name or exit with an error."""
    profile, idx = find_profile(settings, name)
    if profile is None:
        typer.echo(f"Profile '{name}' not found.", err=True)
        raise typer.Exit(1)
    return profile, idx
