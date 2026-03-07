from __future__ import annotations
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

class Font(BaseModel):
    model_config = ConfigDict(extra="allow")
    face: str | None = None
    size: int | None = None

class Profile(BaseModel):
    model_config = ConfigDict(extra="allow")
    guid: str | None = None
    name: str | None = None
    hidden: bool | None = None
    commandline: str | None = None
    source: str | None = None
    font: Font | None = None
    colorScheme: str | None = None
    useAcrylic: bool | None = None
    opacity: int | None = None
    backgroundImage: str | None = None
    backgroundImageOpacity: float | None = None
    backgroundImageStretchMode: str | None = None
    fontFace: str | None = None  # legacy field

class Profiles(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    defaults: dict[str, Any] | None = None
    items: list[Profile] | None = Field(default=None, alias="list")
