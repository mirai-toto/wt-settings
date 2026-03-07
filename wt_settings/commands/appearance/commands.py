import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles.helpers import get_profile_or_abort
from wt_settings.commands.profiles.models import Font

app = typer.Typer(help="Set appearance options for a profile.")

@app.command("font")
def set_font(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    face: str | None = typer.Option(None, "--face", help="Font face name"),
    size: int | None = typer.Option(None, "--size", help="Font size"),
) -> None:
    """Set font face and/or size for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    profile, _ = get_profile_or_abort(settings, profile_name)
    if profile.font is None:
        profile.font = Font()
    if face:
        profile.font.face = face
    if size:
        profile.font.size = size
    config.save(settings)
    typer.echo(f"✓ Font updated for profile '{profile_name}'.")

@app.command("opacity")
def set_opacity(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    value: int = typer.Argument(..., min=0, max=100, help="Opacity percentage (0–100)"),
    acrylic: bool | None = typer.Option(None, "--acrylic/--no-acrylic", help="Enable or disable acrylic"),
) -> None:
    """Set background opacity and optionally toggle acrylic for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    profile, _ = get_profile_or_abort(settings, profile_name)
    profile.opacity = value
    if acrylic is not None:
        profile.useAcrylic = acrylic
    config.save(settings)
    typer.echo(f"✓ Opacity set to {value}% for profile '{profile_name}'.")

@app.command("background")
def set_background(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name"),
    image: str | None = typer.Option(None, "--image", help="Path to background image"),
    opacity: float | None = typer.Option(None, "--opacity", min=0.0, max=1.0, help="Image opacity (0.0–1.0)"),
    stretch: str | None = typer.Option(None, "--stretch", help="Stretch mode: fill, none, uniform, uniformToFill"),
    clear: bool = typer.Option(False, "--clear", help="Remove background image"),
) -> None:
    """Set or clear the background image for a profile."""
    config: Config = ctx.obj
    settings = config.load()
    profile, _ = get_profile_or_abort(settings, profile_name)
    if clear:
        profile.backgroundImage = None
        profile.backgroundImageOpacity = None
        profile.backgroundImageStretchMode = None
        config.save(settings)
        typer.echo(f"✓ Background image cleared for profile '{profile_name}'.")
        return
    if image:
        profile.backgroundImage = image
    if opacity is not None:
        profile.backgroundImageOpacity = opacity
    if stretch:
        valid = {"fill", "none", "uniform", "uniformToFill"}
        if stretch not in valid:
            typer.echo(f"Invalid stretch mode. Choose from: {', '.join(valid)}", err=True)
            raise typer.Exit(1)
        profile.backgroundImageStretchMode = stretch
    config.save(settings)
    typer.echo(f"✓ Background updated for profile '{profile_name}'.")
