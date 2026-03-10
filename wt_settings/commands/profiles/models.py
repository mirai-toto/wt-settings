from __future__ import annotations
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class Font(BaseModel):
    model_config = ConfigDict(extra="allow")
    face: str | None = None
    size: int | None = None
    weight: str | None = None
    features: dict[str, int] | None = None
    axes: dict[str, float] | None = None


class Profile(BaseModel):
    model_config = ConfigDict(extra="allow")
    # General
    guid: str | None = None
    name: str | None = None
    hidden: bool | None = None
    commandline: str | None = None
    source: str | None = None
    startingDirectory: str | None = None
    icon: str | None = None
    tabTitle: str | None = None
    elevate: bool | None = None
    # Appearance - font
    font: Font | None = None
    fontFace: str | None = None  # legacy field
    # Appearance - cursor
    cursorShape: str | None = None
    cursorHeight: int | None = None
    cursorColor: str | None = None
    # Appearance - colors
    colorScheme: str | None = None
    foreground: str | None = None
    background: str | None = None
    selectionBackground: str | None = None
    tabColor: str | None = None
    adjustIndistinguishableColors: str | None = None
    intenseTextStyle: str | None = None
    # Appearance - background image
    backgroundImage: str | None = None
    backgroundImageOpacity: float | None = None
    backgroundImageStretchMode: str | None = None
    backgroundImageAlignment: str | None = None
    # Appearance - transparency
    useAcrylic: bool | None = None
    opacity: int | None = None
    # Appearance - window
    padding: str | None = None
    scrollbarState: str | None = None
    # Advanced
    suppressApplicationTitle: bool | None = None
    antialiasingMode: str | None = None
    altGrAliasing: bool | None = None
    snapOnInput: bool | None = None
    historySize: int | None = None
    closeOnExit: str | None = None
    bellStyle: str | list[str] | None = None
    bellSound: str | list[str] | None = None
    autoMarkPrompts: bool | None = None
    showMarksOnScrollbar: bool | None = None
    pathTranslationStyle: str | None = None


class Profiles(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    defaults: dict[str, Any] | None = None
    items: list[Profile] | None = Field(default=None, alias="list")
