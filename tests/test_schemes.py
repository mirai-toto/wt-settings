import json
from tests.conftest import invoke

NEW_SCHEME = {
    "name": "Monokai",
    "background": "#272822",
    "foreground": "#F8F8F2",
    "black": "#272822",
    "red": "#F92672",
    "green": "#A6E22E",
    "yellow": "#F4BF75",
    "blue": "#66D9EF",
    "purple": "#AE81FF",
    "cyan": "#A1EFE4",
    "white": "#F8F8F2",
    "brightBlack": "#75715E",
    "brightRed": "#F92672",
    "brightGreen": "#A6E22E",
    "brightYellow": "#F4BF75",
    "brightBlue": "#66D9EF",
    "brightPurple": "#AE81FF",
    "brightCyan": "#A1EFE4",
    "brightWhite": "#F9F8F5",
}


def test_list(runner, settings_file):
    result = invoke(runner, settings_file, "scheme", "list")
    assert result.exit_code == 0
    assert "Dark+" in result.output


def test_show(runner, settings_file):
    result = invoke(runner, settings_file, "scheme", "show", "Dark+")
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["name"] == "Dark+"
    assert data["background"] == "#1E1E1E"


def test_show_not_found(runner, settings_file):
    result = invoke(runner, settings_file, "scheme", "show", "DoesNotExist")
    assert result.exit_code == 1


def test_add(runner, settings_file, tmp_path):
    scheme_file = tmp_path / "monokai.json"
    scheme_file.write_text(json.dumps(NEW_SCHEME), encoding="utf-8")

    result = invoke(runner, settings_file, "scheme", "add", str(scheme_file))
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    names = [s["name"] for s in data["schemes"]]
    assert "Monokai" in names


def test_add_duplicate(runner, settings_file, tmp_path):
    scheme_file = tmp_path / "dark.json"
    scheme_file.write_text(json.dumps({**NEW_SCHEME, "name": "Dark+"}), encoding="utf-8")

    result = invoke(runner, settings_file, "scheme", "add", str(scheme_file))
    assert result.exit_code == 1


def test_delete(runner, settings_file):
    result = invoke(runner, settings_file, "scheme", "delete", "Dark+", "--force")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    names = [s["name"] for s in data["schemes"]]
    assert "Dark+" not in names


def test_delete_not_found(runner, settings_file):
    result = invoke(runner, settings_file, "scheme", "delete", "DoesNotExist", "--force")
    assert result.exit_code == 1


def test_apply(runner, settings_file):
    result = invoke(runner, settings_file, "scheme", "apply", "UbuntuWslDev", "Dark+")
    assert result.exit_code == 0

    data = json.loads(settings_file.read_text(encoding="utf-8"))
    profile = next(p for p in data["profiles"]["list"] if p["name"] == "UbuntuWslDev")
    assert profile["colorScheme"] == "Dark+"


def test_add_missing_name(runner, settings_file, tmp_path):
    """Only name is required — scheme without a name must be rejected."""
    scheme = {**NEW_SCHEME}
    del scheme["name"]
    scheme_file = tmp_path / "bad.json"
    scheme_file.write_text(json.dumps(scheme), encoding="utf-8")

    result = invoke(runner, settings_file, "scheme", "add", str(scheme_file))
    assert result.exit_code == 1
