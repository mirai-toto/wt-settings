import json
import shutil
from pathlib import Path
import pytest
from typer.testing import CliRunner
from wt_settings.main import app

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def settings_file(tmp_path):
    path = tmp_path / "settings.json"
    shutil.copy(FIXTURES_DIR / "settings.json", path)
    return path


@pytest.fixture
def runner():
    return CliRunner()


def invoke(runner, settings_file, *args):
    return runner.invoke(app, ["--settings", str(settings_file), *args])