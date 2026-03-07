from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict

class Font(BaseModel):
    model_config = ConfigDict(extra="allow")
    face: Optional[str] = None
    size: Optional[int] = None

class Profile(BaseModel):
    model_config = ConfigDict(extra="allow")
    guid: Optional[str] = None
    name: Optional[str] = None
    hidden: Optional[bool] = None
    commandline: Optional[str] = None
    source: Optional[str] = None
    font: Optional[Font] = None
    colorScheme: Optional[str] = None
    useAcrylic: Optional[bool] = None
    opacity: Optional[int] = None
    backgroundImage: Optional[str] = None
    backgroundImageOpacity: Optional[float] = None
    backgroundImageStretchMode: Optional[str] = None
    fontFace: Optional[str] = None  # legacy field

class Profiles(BaseModel):
    model_config = ConfigDict(extra="allow")
    defaults: Optional[dict[str, Any]] = None
    list: Optional[list[Profile]] = None
