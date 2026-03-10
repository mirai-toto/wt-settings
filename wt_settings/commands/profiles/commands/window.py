from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.enums import ScrollbarState


def set_window(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    padding: str | None = typer.Option(
        None, "--padding", help="Padding around text (e.g. '8' or '8, 8, 8, 8')"
    ),
    scrollbar: ScrollbarState | None = typer.Option(
        None, "--scrollbar", help="Scrollbar state"
    ),
) -> None:
    """Set window appearance for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if padding is not None:
        profile.padding = padding
    if scrollbar is not None:
        profile.scrollbarState = scrollbar.value
    config.save(settings)
    typer.echo(f"✓ Window settings updated for profile '{profile_name}'.")
