from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Profile:
    name: str
    selected_flags: list[str] = field(default_factory=list)
    customizations: dict[str, object] = field(default_factory=dict)


class ProfileManager:
    def __init__(self, config) -> None:
        self.config = config

    def list_profiles(self) -> list[dict[str, object]]:
        return list(self.config.data.profiles or [])

    def get_active_profile(self) -> dict[str, object]:
        return self.config.get_active_profile()

    def create_profile(self, name: str) -> dict[str, object]:
        profiles = list(self.config.data.profiles or [])
        if any(profile.get("name") == name for profile in profiles):
            raise ValueError(f"Profile '{name}' already exists.")
        profile = {"name": name, "selected_flags": [], "customizations": {}}
        profiles.append(profile)
        self.config.data.profiles = profiles
        self.config.save(self.config.data)
        return profile

    def switch_profile(self, name: str) -> dict[str, object]:
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                self.config.set_active_profile(name)
                return profile
        raise ValueError(f"Profile '{name}' was not found.")

    def delete_profile(self, name: str) -> None:
        profiles = [profile for profile in self.list_profiles() if profile.get("name") != name]
        if not profiles:
            raise ValueError("At least one profile must remain.")
        self.config.data.profiles = profiles
        if self.config.data.active_profile == name:
            self.config.data.active_profile = profiles[0].get("name", "Default")
        self.config.save(self.config.data)
