from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class AppConfig:
    studio_install_path: str | None = None
    active_profile: str = "Default"
    theme: str = "dark"
    profiles: list[dict[str, Any]] | None = None
    fast_flags: dict[str, bool] | None = None
    recent_activities: list[dict[str, str]] | None = None

    @classmethod
    def defaults(cls) -> "AppConfig":
        return cls(
            studio_install_path=None,
            active_profile="Default",
            theme="dark",
            profiles=[
                {
                    "name": "Default",
                    "selected_flags": [],
                    "customizations": {"theme": "dark"},
                },
                {
                    "name": "Performance",
                    "selected_flags": ["DFFlagDebugGraphicsEnable", "DFFlagFixGraphicsQuality"],
                    "customizations": {"theme": "dark", "compact_sidebar": True},
                },
            ],
            fast_flags={
                "DFFlagDebugGraphicsEnable": False,
                "DFFlagFixGraphicsQuality": True,
                "DFIntTaskSchedulerTargetFrameRate": True,
                "DFIntUseFastFlag": True,
            },
            recent_activities=[],
        )


class ConfigStore:
    def __init__(self, root_dir: str | Path | None = None) -> None:
        self.root_dir = Path(root_dir) if root_dir else Path.home() / ".modifystrap"
        self.config_path = self.root_dir / "config.json"
        self.backups_dir = self.root_dir / "backups"
        self.activity_dir = self.root_dir / "activity"
        self.ensure_storage()
        self._data = self.load()

    def ensure_storage(self) -> None:
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        self.activity_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self.save(AppConfig.defaults())

    def load(self) -> AppConfig:
        if not self.config_path.exists():
            return AppConfig.defaults()
        with self.config_path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        return AppConfig(**payload)

    def save(self, config: AppConfig | None = None) -> AppConfig:
        normalized = config or self._data
        self._data = normalized
        with self.config_path.open("w", encoding="utf-8") as file:
            json.dump(asdict(normalized), file, indent=2, sort_keys=True)
        return self._data

    def update(self, **kwargs: Any) -> AppConfig:
        for key, value in kwargs.items():
            setattr(self._data, key, value)
        return self.save(self._data)

    @property
    def data(self) -> AppConfig:
        return self._data

    @property
    def theme(self) -> str:
        return self._data.theme

    @theme.setter
    def theme(self, value: str) -> None:
        self._data.theme = value
        self.save(self._data)

    def get_active_profile(self) -> dict[str, Any]:
        profiles = self._data.profiles or []
        active_name = self._data.active_profile
        for profile in profiles:
            if profile.get("name") == active_name:
                return profile
        return profiles[0] if profiles else {"name": "Default", "selected_flags": [], "customizations": {}}

    def set_active_profile(self, name: str) -> None:
        self._data.active_profile = name
        self.save(self._data)

    def get_fast_flags(self) -> dict[str, bool]:
        flags = self._data.fast_flags or {}
        return dict(flags)

    def set_fast_flags(self, fast_flags: dict[str, bool]) -> None:
        self._data.fast_flags = dict(fast_flags)
        self.save(self._data)

    def get_recent_activities(self) -> list[dict[str, str]]:
        return list(self._data.recent_activities or [])

    def record_activity(self, message: str, level: str = "info") -> None:
        activities = list(self._data.recent_activities or [])
        activities.append({"message": message, "level": level})
        if len(activities) > 20:
            activities = activities[-20:]
        self._data.recent_activities = activities
        self.save(self._data)
