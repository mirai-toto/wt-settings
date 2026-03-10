import typer
from .crud import list_profiles, show_profile, add_profile, delete_profile
from .font import set_font
from .cursor import set_cursor
from .bell import set_bell
from .background import set_background
from .opacity import set_opacity
from .colors import set_colors
from .window import set_window
from .advanced import set_advanced

app = typer.Typer(help="Manage Windows Terminal profiles.")

app.command("list")(list_profiles)
app.command("show")(show_profile)
app.command("add")(add_profile)
app.command("delete")(delete_profile)
app.command("font")(set_font)
app.command("cursor")(set_cursor)
app.command("bell")(set_bell)
app.command("background")(set_background)
app.command("opacity")(set_opacity)
app.command("colors")(set_colors)
app.command("window")(set_window)
app.command("advanced")(set_advanced)
