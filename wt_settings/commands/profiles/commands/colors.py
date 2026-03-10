from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.enums import IntenseTextStyle


def set_colors(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    scheme: str | None = typer.Option(None, "--scheme", help="Color scheme name"),
    foreground: str | None = typer.Option(
        None, "--foreground", help="Foreground color (hex)"
    ),
    background: str | None = typer.Option(
        None, "--background", help="Background color (hex)"
    ),
    selection_bg: str | None = typer.Option(
        None, "--selection-bg", help="Selection background color (hex)"
    ),
    tab_color: str | None = typer.Option(None, "--tab-color", help="Tab color (hex)"),
    adjust_indistinguishable: str | None = typer.Option(
        None,
        "--adjust-indistinguishable",
        help="Adjust indistinguishable colors (never, always, indexed)",
    ),
    intense_style: IntenseTextStyle | None = typer.Option(
        None, "--intense-style", help="Intense text style"
    ),
) -> None:
    """Set color settings for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if scheme is not None:
        profile.colorScheme = scheme
    if foreground is not None:
        profile.foreground = foreground
    if background is not None:
        profile.background = background
    if selection_bg is not None:
        profile.selectionBackground = selection_bg
    if tab_color is not None:
        profile.tabColor = tab_color
    if adjust_indistinguishable is not None:
        profile.adjustIndistinguishableColors = adjust_indistinguishable
    if intense_style is not None:
        profile.intenseTextStyle = intense_style.value
    config.save(settings)
    typer.echo(f"✓ Colors updated for profile '{profile_name}'.")
