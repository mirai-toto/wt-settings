from __future__ import annotations
from wt_settings.commands.schemes.models import ColorScheme
from wt_settings.core.models import Settings


class SchemeNotFound(Exception):
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"Scheme '{self.name}' not found."


def find(settings: Settings, name: str) -> ColorScheme | None:
    return next((s for s in (settings.schemes or []) if s.name == name), None)


def get(settings: Settings, name: str) -> ColorScheme:
    scheme = find(settings, name)
    if scheme is None:
        raise SchemeNotFound(name)
    return scheme
