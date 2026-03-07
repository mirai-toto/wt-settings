from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ColorScheme(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: Optional[str] = None
    background: Optional[str] = None
    foreground: Optional[str] = None
    black: Optional[str] = None
    red: Optional[str] = None
    green: Optional[str] = None
    yellow: Optional[str] = None
    blue: Optional[str] = None
    purple: Optional[str] = None
    cyan: Optional[str] = None
    white: Optional[str] = None
    brightBlack: Optional[str] = None
    brightRed: Optional[str] = None
    brightGreen: Optional[str] = None
    brightYellow: Optional[str] = None
    brightBlue: Optional[str] = None
    brightPurple: Optional[str] = None
    brightCyan: Optional[str] = None
    brightWhite: Optional[str] = None
