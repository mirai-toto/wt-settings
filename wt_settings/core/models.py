from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from wt_settings.commands.profiles.models import Profiles
from wt_settings.commands.schemes.models import ColorScheme

class Action(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Any = None
    id: Optional[str] = None

class Keybinding(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: Optional[str] = None
    keys: Optional[str] = None

class NewTabMenuItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: Optional[str] = None

class Settings(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    help_url: Optional[str] = Field(None, alias="$help")
    schema_url: Optional[str] = Field(None, alias="$schema")
    actions: Optional[list[Action]] = None
    copyFormatting: Optional[str] = None
    copyOnSelect: Optional[bool] = None
    defaultProfile: Optional[str] = None
    keybindings: Optional[list[Keybinding]] = None
    newTabMenu: Optional[list[NewTabMenuItem]] = None
    profiles: Optional[Profiles] = None
    schemes: Optional[list[ColorScheme]] = None
    themes: Optional[list[Any]] = None
