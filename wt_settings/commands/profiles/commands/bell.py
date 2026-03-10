from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.enums import BellStyle


def set_bell(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    style: BellStyle | None = typer.Option(None, "--style", help="Bell style"),
    sound: str | None = typer.Option(
        None, "--sound", help="Path to audio file for bell sound"
    ),
    disable: bool = typer.Option(False, "--disable", help="Shorthand for --style none"),
) -> None:
    """Set bell style and sound for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if disable:
        profile.bellStyle = BellStyle.none.value
    elif style is not None:
        profile.bellStyle = style.value
    if sound is not None:
        profile.bellSound = sound
    config.save(settings)
    typer.echo(f"✓ Bell updated for profile '{profile_name}'.")
