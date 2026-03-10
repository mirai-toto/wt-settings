import json
from tests.conftest import invoke


def test_round_trip(runner, settings_file):
    """Reading and writing settings.json must not lose any data."""
    before = json.loads(settings_file.read_text(encoding="utf-8"))

    # Trigger a read+write by making a no-op change
    invoke(runner, settings_file, "profile", "font", "UbuntuWsl", "--face", "DroidSansM Nerd Font Mono")

    after = json.loads(settings_file.read_text(encoding="utf-8"))

    # Global fields preserved
    assert after["$schema"] == before["$schema"]
    assert after["$help"] == before["$help"]
    assert after["defaultProfile"] == before["defaultProfile"]
    assert after["copyFormatting"] == before["copyFormatting"]
    assert after["copyOnSelect"] == before["copyOnSelect"]

    # Actions and keybindings preserved
    assert after["actions"] == before["actions"]
    assert after["keybindings"] == before["keybindings"]
    assert after["newTabMenu"] == before["newTabMenu"]
    assert after["themes"] == before["themes"]

    # All profiles preserved
    assert len(after["profiles"]["list"]) == len(before["profiles"]["list"])


def test_bom_not_written(runner, settings_file):
    """Output file must not contain a BOM."""
    invoke(runner, settings_file, "profile", "list")
    raw = settings_file.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")


def test_unknown_profile_fields_preserved(runner, settings_file):
    """Fields not in the model (extra='allow') must survive a round-trip."""
    data = json.loads(settings_file.read_text(encoding="utf-8"))
    data["profiles"]["list"][0]["someUnknownField"] = "shouldBeKept"
    settings_file.write_text(json.dumps(data), encoding="utf-8")

    invoke(runner, settings_file, "profile", "font", "Windows PowerShell", "--size", "12")

    after = json.loads(settings_file.read_text(encoding="utf-8"))
    ps_profile = next(p for p in after["profiles"]["list"] if p["name"] == "Windows PowerShell")
    assert ps_profile["someUnknownField"] == "shouldBeKept"
