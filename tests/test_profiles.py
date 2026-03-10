import json
from tests.conftest import invoke


# ── CRUD ──────────────────────────────────────────────────────────────────────


def test_list(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "list")
    assert result.exit_code == 0
    assert "UbuntuWsl" in result.output
    assert "UbuntuWslDev" in result.output
    assert "Windows PowerShell" in result.output


def test_show(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "show", "UbuntuWsl")
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["name"] == "UbuntuWsl"
    assert data["colorScheme"] == "Dark+"
    assert data["opacity"] == 80


def test_show_not_found(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "show", "DoesNotExist")
    assert result.exit_code == 1


def test_add(runner, settings_file):
    result = invoke(
        runner,
        settings_file,
        "profile",
        "add",
        "MyProfile",
        "--commandline",
        "zsh",
        "--starting-directory",
        "~",
        "--tab-title",
        "Dev",
    )
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profiles = data["profiles"]["list"]
    added = next((p for p in profiles if p["name"] == "MyProfile"), None)
    assert added is not None
    assert added["commandline"] == "zsh"
    assert added["startingDirectory"] == "~"
    assert added["tabTitle"] == "Dev"
    assert "guid" in added


def test_add_duplicate(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "add", "UbuntuWsl")
    assert result.exit_code == 1


def test_delete(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "delete", "UbuntuWslDev", "--force")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    names = [p["name"] for p in data["profiles"]["list"]]
    assert "UbuntuWslDev" not in names


def test_delete_not_found(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "delete", "DoesNotExist", "--force")
    assert result.exit_code == 1


# ── FONT ──────────────────────────────────────────────────────────────────────


def test_font(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "font", "Windows PowerShell", "--face", "Cascadia Code", "--size", "13", "--weight", "bold")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    ps = next(p for p in data["profiles"]["list"] if p["name"] == "Windows PowerShell")
    assert ps["font"]["face"] == "Cascadia Code"
    assert ps["font"]["size"] == 13
    assert ps["font"]["weight"] == "bold"


# ── CURSOR ────────────────────────────────────────────────────────────────────


def test_cursor(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "cursor", "UbuntuWsl", "--shape", "filledBox", "--color", "#ffffff")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["cursorShape"] == "filledBox"
    assert profile["cursorColor"] == "#ffffff"


def test_cursor_invalid_shape(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "cursor", "UbuntuWsl", "--shape", "invalid")
    assert result.exit_code != 0


# ── BELL ──────────────────────────────────────────────────────────────────────


def test_bell_style(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "bell", "UbuntuWsl", "--style", "audible")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["bellStyle"] == "audible"


def test_bell_disable(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "bell", "UbuntuWsl", "--disable")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["bellStyle"] == "none"


def test_bell_sound(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "bell", "UbuntuWsl", "--sound", "C:/sounds/bell.wav")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["bellSound"] == "C:/sounds/bell.wav"


# ── BACKGROUND ────────────────────────────────────────────────────────────────


def test_background_set(runner, settings_file):
    result = invoke(
        runner,
        settings_file,
        "profile",
        "background",
        "UbuntuWsl",
        "--image",
        "C:/bg.png",
        "--opacity",
        "0.3",
        "--stretch",
        "uniformToFill",
        "--alignment",
        "center",
    )
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["backgroundImage"] == "C:/bg.png"
    assert profile["backgroundImageOpacity"] == 0.3
    assert profile["backgroundImageStretchMode"] == "uniformToFill"
    assert profile["backgroundImageAlignment"] == "center"


def test_background_clear(runner, settings_file):
    # First set a background
    invoke(runner, settings_file, "profile", "background", "UbuntuWsl", "--image", "C:/bg.png")
    # Then clear it
    result = invoke(runner, settings_file, "profile", "background", "UbuntuWsl", "--clear")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert "backgroundImage" not in profile


# ── OPACITY ───────────────────────────────────────────────────────────────────


def test_opacity(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "opacity", "UbuntuWsl", "50", "--acrylic")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["opacity"] == 50
    assert profile["useAcrylic"] is True


# ── COLORS ────────────────────────────────────────────────────────────────────


def test_colors(runner, settings_file):
    result = invoke(
        runner,
        settings_file,
        "profile",
        "colors",
        "UbuntuWsl",
        "--foreground",
        "#d4d4d4",
        "--background",
        "#1e1e1e",
        "--tab-color",
        "#ff0000",
    )
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["foreground"] == "#d4d4d4"
    assert profile["background"] == "#1e1e1e"
    assert profile["tabColor"] == "#ff0000"


# ── WINDOW ────────────────────────────────────────────────────────────────────


def test_window(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "window", "UbuntuWsl", "--padding", "8", "--scrollbar", "hidden")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["padding"] == "8"
    assert profile["scrollbarState"] == "hidden"


def test_window_invalid_scrollbar(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "window", "UbuntuWsl", "--scrollbar", "invalid")
    assert result.exit_code != 0


# ── ADVANCED ──────────────────────────────────────────────────────────────────


def test_advanced(runner, settings_file):
    result = invoke(
        runner,
        settings_file,
        "profile",
        "advanced",
        "UbuntuWsl",
        "--history-size",
        "9001",
        "--close-on-exit",
        "graceful",
        "--antialiasing",
        "cleartype",
        "--suppress-title",
    )
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWsl")
    assert profile["historySize"] == 9001
    assert profile["closeOnExit"] == "graceful"
    assert profile["antialiasingMode"] == "cleartype"
    assert profile["suppressApplicationTitle"] is True


def test_advanced_invalid_close_on_exit(runner, settings_file):
    result = invoke(runner, settings_file, "profile", "advanced", "UbuntuWsl", "--close-on-exit", "invalid")
    assert result.exit_code != 0
