from __future__ import annotations
from pydantic import BaseModel, ConfigDict


class ColorScheme(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str | None = None
    background: str | None = None
    foreground: str | None = None
    black: str | None = None
    red: str | None = None
    green: str | None = None
    yellow: str | None = None
    blue: str | None = None
    purple: str | None = None
    cyan: str | None = None
    white: str | None = None
    brightBlack: str | None = None
    brightRed: str | None = None
    brightGreen: str | None = None
    brightYellow: str | None = None
    brightBlue: str | None = None
    brightPurple: str | None = None
    brightCyan: str | None = None
    brightWhite: str | None = None
