import json
import uuid
import typer
from wt_settings.core.config import Config
from wt_settings.commands.profiles.helpers import find_profile, get_profile_or_abort
from wt_settings.commands.profiles.models import Profile, Profiles

app = typer.Typer(help="Manage Windows Terminal profiles.")

@app.command("list")
def list_profiles(ctx: typer.Context) -> None:
    """List all profiles."""
    config: Config = ctx.obj
    settings = config.load()
    profiles = (settings.profiles and settings.profiles.list) or []
    if not profiles:
        typer.echo("No profiles found.")
        return
    for p in profiles:
        hidden = " [hidden]" if p.hidden else ""
        typer.echo(f"  • {p.name or '<unnamed>'} {p.guid or ''}{hidden}")

@app.command("show")
def show_profile(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Profile name"),
) -> None:
    """Show all settings for a specific profile."""
    config: Config = ctx.obj
    settings = config.load()
    profile, _ = get_profile_or_abort(settings, name)
    typer.echo(json.dumps(profile.model_dump(by_alias=True, exclude_none=True), indent=4))

@app.command("add")
def add_profile(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Profile name"),
    guid: str | None = typer.Option(None, help="Optional GUID (auto-generated if omitted)"),
    commandline: str | None = typer.Option(None, help="Shell command line"),
) -> None:
    """Add a new profile."""
    config: Config = ctx.obj
    settings = config.load()
    existing, _ = find_profile(settings, name)
    if existing is not None:
        typer.echo(f"Profile '{name}' already exists.", err=True)
        raise typer.Exit(1)
    new_profile = Profile(
        name=name,
        guid=guid or "{" + str(uuid.uuid4()) + "}",
        commandline=commandline,
    )
    if settings.profiles is None:
        settings.profiles = Profiles(list=[])
    if settings.profiles.list is None:
        settings.profiles.list = []
    settings.profiles.list.append(new_profile)
    config.save(settings)
    typer.echo(f"✓ Profile '{name}' added.")

@app.command("delete")
def delete_profile(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Profile name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Delete a profile by name."""
    config: Config = ctx.obj
    settings = config.load()
    _, idx = find_profile(settings, name)
    if idx == -1:
        typer.echo(f"Profile '{name}' not found.", err=True)
        raise typer.Exit(1)
    if not force:
        typer.confirm(f"Delete profile '{name}'?", abort=True)
    settings.profiles.list.pop(idx)
    config.save(settings)
    typer.echo(f"✓ Profile '{name}' deleted.")
