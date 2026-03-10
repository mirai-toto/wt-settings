from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.enums import (
    BackgroundAlignment,
    BackgroundStretchMode,
)


def set_background(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    image: str | None = typer.Option(None, "--image", help="Path to background image"),
    opacity: float | None = typer.Option(
        None, "--opacity", min=0.0, max=1.0, help="Image opacity (0.0–1.0)"
    ),
    stretch: BackgroundStretchMode | None = typer.Option(
        None, "--stretch", help="Stretch mode"
    ),
    alignment: BackgroundAlignment | None = typer.Option(
        None, "--alignment", help="Image alignment"
    ),
    clear: bool = typer.Option(False, "--clear", help="Remove background image"),
) -> None:
    """Set or clear the background image for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if clear:
        profile.backgroundImage = None
        profile.backgroundImageOpacity = None
        profile.backgroundImageStretchMode = None
        profile.backgroundImageAlignment = None
        config.save(settings)
        typer.echo(f"✓ Background image cleared for profile '{profile_name}'.")
        return
    if image is not None:
        profile.backgroundImage = image
    if opacity is not None:
        profile.backgroundImageOpacity = opacity
    if stretch is not None:
        profile.backgroundImageStretchMode = stretch.value
    if alignment is not None:
        profile.backgroundImageAlignment = alignment.value
    config.save(settings)
    typer.echo(f"✓ Background updated for profile '{profile_name}'.")
