from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.models import Font


def set_font(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    face: str | None = typer.Option(None, "--face", help="Font face name"),
    size: int | None = typer.Option(None, "--size", help="Font size"),
    weight: str | None = typer.Option(
        None,
        "--weight",
        help="Font weight (e.g. normal, bold, thin, light, semi-bold, extra-bold)",
    ),
) -> None:
    """Set font for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if profile.font is None:
        profile.font = Font()
    if face is not None:
        profile.font.face = face
    if size is not None:
        profile.font.size = size
    if weight is not None:
        profile.font.weight = weight
    config.save(settings)
    typer.echo(f"✓ Font updated for profile '{profile_name}'.")
