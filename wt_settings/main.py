from pathlib import Path
import typer
from wt_settings.commands.profiles.commands import app as profiles_app
from wt_settings.commands.schemes.commands import app as schemes_app
from wt_settings.core.config import Config
from wt_settings.core.storage import discover_settings_path

app = typer.Typer(
    name="wts",
    help="wt-settings — A CLI to read and write Windows Terminal settings.json",
    no_args_is_help=True,
)
app.add_typer(profiles_app, name="profile")
app.add_typer(schemes_app, name="scheme")


@app.callback()
def callback(
    ctx: typer.Context,
    settings: Path | None = typer.Option(
        None,
        "--settings",
        help="Path to Windows Terminal settings.json. Auto-discovered if not provided.",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print what would be saved without writing."
    ),
) -> None:
    try:
        path = settings or discover_settings_path()
    except (EnvironmentError, FileNotFoundError) as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(1)
    ctx.obj = Config(settings_path=path, dry_run=dry_run)


@app.command("path")
def show_path(ctx: typer.Context) -> None:
    """Print the resolved path to settings.json."""
    config: Config = ctx.obj
    typer.echo(str(config.settings_path))


if __name__ == "__main__":
    app()
