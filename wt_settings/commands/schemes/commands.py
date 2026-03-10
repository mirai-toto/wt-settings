from __future__ import annotations
import json
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service as profile_service
from wt_settings.commands.schemes import service
from wt_settings.commands.schemes.models import ColorScheme

app = typer.Typer(help="Manage color schemes.")


@app.command("list")
def list_schemes(ctx: typer.Context) -> None:
    """List all color schemes."""
    config: Config = ctx.obj
    settings = config.load()
    schemes = settings.schemes or []
    if not schemes:
        typer.echo("No color schemes found.")
        return
    for s in schemes:
        typer.echo(f"  • {s.name or '<unnamed>'}")


@app.command("show")
def show_scheme(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Scheme name"),
) -> None:
    """Show all colors in a scheme."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        scheme = service.get(settings, name)
    except service.SchemeNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    typer.echo(
        json.dumps(scheme.model_dump(by_alias=True, exclude_none=True), indent=4)
    )


@app.command("add")
def add_scheme(
    ctx: typer.Context,
    file: typer.FileText = typer.Argument(
        ..., help="Path to a JSON file containing the scheme"
    ),
) -> None:
    """Add a color scheme from a JSON file."""
    try:
        data = json.load(file)
    except json.JSONDecodeError as e:
        typer.echo(f"Invalid JSON: {e}", err=True)
        raise typer.Exit(1)
    if "name" not in data:
        typer.echo("Scheme JSON must include a 'name' field.", err=True)
        raise typer.Exit(1)
    scheme = ColorScheme.model_validate(data)
    config: Config = ctx.obj
    settings = config.load()
    if settings.schemes is None:
        settings.schemes = []
    if service.find(settings, scheme.name):
        typer.echo(
            f"Scheme '{scheme.name}' already exists. Use 'delete' first to replace it.",
            err=True,
        )
        raise typer.Exit(1)
    settings.schemes.append(scheme)
    config.save(settings)
    typer.echo(f"✓ Scheme '{scheme.name}' added.")


@app.command("delete")
def delete_scheme(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Scheme name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Delete a color scheme by name."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        scheme = service.get(settings, name)
    except service.SchemeNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if not force:
        typer.confirm(f"Delete scheme '{name}'?", abort=True)
    settings.schemes.remove(scheme)
    config.save(settings)
    typer.echo(f"✓ Scheme '{name}' deleted.")


@app.command("apply")
def apply_scheme(
    ctx: typer.Context,
    profile_name: str = typer.Argument(..., help="Profile name to apply the scheme to"),
    scheme_name: str = typer.Argument(..., help="Color scheme name"),
) -> None:
    """Apply a color scheme to a profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = profile_service.get(settings, profile_name)
    except profile_service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    profile.colorScheme = scheme_name
    config.save(settings)
    typer.echo(f"✓ Scheme '{scheme_name}' applied to profile '{profile_name}'.")
