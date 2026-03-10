from __future__ import annotations
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from wt_settings.commands.profiles.models import Profiles
from wt_settings.commands.schemes.models import ColorScheme


class Action(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Any = None
    id: str | None = None


class Keybinding(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str | None = None
    keys: str | None = None


class NewTabMenuItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str | None = None


class Settings(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    help_url: str | None = Field(None, alias="$help")
    schema_url: str | None = Field(None, alias="$schema")
    actions: list[Action] | None = None
    copyFormatting: str | None = None
    copyOnSelect: bool | None = None
    defaultProfile: str | None = None
    keybindings: list[Keybinding] | None = None
    newTabMenu: list[NewTabMenuItem] | None = None
    profiles: Profiles | None = None
    schemes: list[ColorScheme] | None = None
    themes: list[Any] | None = None
