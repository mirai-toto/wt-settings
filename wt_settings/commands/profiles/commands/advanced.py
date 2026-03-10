from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.enums import (
    AntialiasingMode,
    CloseOnExit,
    PathTranslationStyle,
)


def set_advanced(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    suppress_title: bool | None = typer.Option(
        None,
        "--suppress-title/--no-suppress-title",
        help="Suppress application title changes",
    ),
    antialiasing: AntialiasingMode | None = typer.Option(
        None, "--antialiasing", help="Text antialiasing mode"
    ),
    altgr_aliasing: bool | None = typer.Option(
        None, "--altgr-aliasing/--no-altgr-aliasing", help="Treat Ctrl+Alt as AltGr"
    ),
    snap_on_input: bool | None = typer.Option(
        None, "--snap-on-input/--no-snap-on-input", help="Scroll to input when typing"
    ),
    history_size: int | None = typer.Option(
        None, "--history-size", help="Scrollback history line count"
    ),
    close_on_exit: CloseOnExit | None = typer.Option(
        None, "--close-on-exit", help="Close on exit mode"
    ),
    auto_mark_prompts: bool | None = typer.Option(
        None,
        "--auto-mark-prompts/--no-auto-mark-prompts",
        help="Automatically add scroll marks at prompts",
    ),
    show_marks: bool | None = typer.Option(
        None, "--show-marks/--no-show-marks", help="Show scroll marks on scrollbar"
    ),
    path_translation: PathTranslationStyle | None = typer.Option(
        None, "--path-translation", help="Path translation style"
    ),
) -> None:
    """Set advanced settings for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if suppress_title is not None:
        profile.suppressApplicationTitle = suppress_title
    if antialiasing is not None:
        profile.antialiasingMode = antialiasing.value
    if altgr_aliasing is not None:
        profile.altGrAliasing = altgr_aliasing
    if snap_on_input is not None:
        profile.snapOnInput = snap_on_input
    if history_size is not None:
        profile.historySize = history_size
    if close_on_exit is not None:
        profile.closeOnExit = close_on_exit.value
    if auto_mark_prompts is not None:
        profile.autoMarkPrompts = auto_mark_prompts
    if show_marks is not None:
        profile.showMarksOnScrollbar = show_marks
    if path_translation is not None:
        profile.pathTranslationStyle = path_translation.value
    config.save(settings)
    typer.echo(f"✓ Advanced settings updated for profile '{profile_name}'.")
