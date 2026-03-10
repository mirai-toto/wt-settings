from __future__ import annotations
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service


def set_opacity(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    value: int = typer.Argument(..., min=0, max=100, help="Opacity percentage (0–100)"),
    acrylic: bool | None = typer.Option(
        None, "--acrylic/--no-acrylic", help="Enable or disable acrylic"
    ),
) -> None:
    """Set background opacity and optionally toggle acrylic for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, profile_name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    profile.opacity = value
    if acrylic is not None:
        profile.useAcrylic = acrylic
    config.save(settings)
    typer.echo(f"✓ Opacity set to {value}% for profile '{profile_name}'.")
