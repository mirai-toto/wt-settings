from pathlib import Path
from pydantic import BaseModel
from wt_settings.core.models import Settings
from wt_settings.core.storage import load_settings, save_settings


class Config(BaseModel):
    settings_path: Path
    dry_run: bool = False

    def load(self) -> Settings:
        return load_settings(self.settings_path)

    def save(self, settings: Settings) -> None:
        save_settings(settings, self.settings_path, self.dry_run)
