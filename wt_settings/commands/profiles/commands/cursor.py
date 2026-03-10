from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.enums import CursorShape


def set_cursor(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    shape: CursorShape | None = typer.Option(None, "--shape", help="Cursor shape"),
    height: int | None = typer.Option(
        None,
        "--height",
        min=1,
        max=100,
        help="Cursor height percentage (vintage cursor only)",
    ),
    color: str | None = typer.Option(
        None, "--color", help="Cursor color (hex, e.g. #ffffff)"
    ),
) -> None:
    """Set cursor appearance for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if shape is not None:
        profile.cursorShape = shape.value
    if height is not None:
        profile.cursorHeight = height
    if color is not None:
        profile.cursorColor = color
    config.save(settings)
    typer.echo(f"✓ Cursor updated for profile '{profile_name}'.")
