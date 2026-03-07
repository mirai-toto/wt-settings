from __future__ import annotations
from wt_settings.commands.profiles.models import Profile
from wt_settings.core.models import Settings

class ProfileNotFound(Exception):
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"Profile '{self.name}' not found."

def find(settings: Settings, name: str) -> Profile | None:
    return next(
        (p for p in (settings.profiles and settings.profiles.items) or [] if p.name == name),
        None,
    )

def get(settings: Settings, name: str) -> Profile:
    profile = find(settings, name)
    if profile is None:
        raise ProfileNotFound(name)
    return profile
