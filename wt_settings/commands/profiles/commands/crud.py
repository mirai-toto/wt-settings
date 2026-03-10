from __future__ import annotations
import json
import uuid
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles import service
from wt_settings.commands.profiles.models import Profile, Profiles


def list_profiles(ctx: typer.Context) -> None:
    """List all profiles."""
    config: Config = ctx.obj
    settings = config.load()
    profiles = (settings.profiles and settings.profiles.items) or []
    if not profiles:
        typer.echo("No profiles found.")
        return
    for p in profiles:
        hidden = " [hidden]" if p.hidden else ""
        typer.echo(f"  • {p.name or '<unnamed>'} {p.guid or ''}{hidden}")


def show_profile(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Profile name"),
) -> None:
    """Show all settings for a specific profile."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    typer.echo(
        json.dumps(profile.model_dump(by_alias=True, exclude_none=True), indent=4)
    )


def add_profile(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Profile name"),
    guid: str | None = typer.Option(
        None, help="Optional GUID (auto-generated if omitted)"
    ),
    commandline: str | None = typer.Option(None, help="Shell command line"),
    starting_directory: str | None = typer.Option(
        None, "--starting-directory", help="Starting directory"
    ),
    icon: str | None = typer.Option(None, "--icon", help="Icon path or emoji"),
    tab_title: str | None = typer.Option(None, "--tab-title", help="Tab title"),
    elevate: bool | None = typer.Option(
        None, "--elevate/--no-elevate", help="Run as administrator"
    ),
) -> None:
    """Add a new profile."""
    config: Config = ctx.obj
    settings = config.load()
    if service.find(settings, name) is not None:
        typer.echo(f"Profile '{name}' already exists.", err=True)
        raise typer.Exit(1)
    new_profile = Profile(
        name=name,
        guid=guid or "{" + str(uuid.uuid4()) + "}",
        commandline=commandline,
        startingDirectory=starting_directory,
        icon=icon,
        tabTitle=tab_title,
        elevate=elevate,
    )
    if settings.profiles is None:
        settings.profiles = Profiles(items=[])
    settings.profiles.items.append(new_profile)
    config.save(settings)
    typer.echo(f"✓ Profile '{name}' added.")


def delete_profile(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Profile name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Delete a profile by name."""
    config: Config = ctx.obj
    settings = config.load()
    try:
        profile = service.get(settings, name)
    except service.ProfileNotFound as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    if not force:
        typer.confirm(f"Delete profile '{name}'?", abort=True)
    settings.profiles.items.remove(profile)
    config.save(settings)
    typer.echo(f"✓ Profile '{name}' deleted.")
