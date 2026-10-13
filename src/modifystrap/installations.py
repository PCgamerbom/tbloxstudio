from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Installation:
    name: str
    path: str
    version: str
    executable: str | None = None

    @property
    def resolved_path(self) -> Path:
        return Path(self.path)

    def is_valid(self) -> bool:
        path = self.resolved_path
        if not path.exists():
            return False
        if self.executable:
            return (path / self.executable).exists() or Path(self.executable).exists()
        return True


class InstallationManager:
    def __init__(self, config) -> None:
        self.config = config

    def detect_installations(self) -> list[Installation]:
        candidates: list[Installation] = []
        roots: list[Path] = []

        if os.name == "nt":
            user_profile = Path.home()
            roots.extend(
                [
                    user_profile / "AppData" / "Local" / "Roblox" / "Versions",
                    Path("C:/Program Files/Roblox/Versions"),
                    Path("C:/Program Files (x86)/Roblox/Versions"),
                ]
            )
        else:
            roots.extend(
                [
                    Path.home() / ".local" / "share" / "Roblox" / "Versions",
                    Path.home() / ".roblox" / "Versions",
                    Path("/opt/roblox/Versions"),
                ]
            )

        for root in roots:
            if not root.exists():
                continue
            for child in sorted(root.iterdir()):
                if not child.is_dir():
                    continue
                installation = self._inspect_directory(child)
                if installation:
                    candidates.append(installation)

        maybe_parents = set()
        for candidate in [self.config.root_dir, self.config.root_dir.parent, Path.cwd()]:
            if candidate.exists():
                maybe_parents.add(candidate)
        for base_dir in sorted(maybe_parents):
            if base_dir.is_file():
                continue
            for child in sorted(base_dir.iterdir()):
                if not child.is_dir():
                    continue
                installation = self._inspect_directory(child)
                if installation and installation not in candidates:
                    candidates.append(installation)

        configured = self.config.data.studio_install_path
        if configured:
            path = Path(configured)
            if path.exists():
                installation = self._inspect_directory(path)
                if installation and installation not in candidates:
                    candidates.append(installation)

        return candidates

    def _inspect_directory(self, directory: Path) -> Installation | None:
        executable_names = [
            "RobloxStudioBeta.exe",
            "RobloxStudioLauncher.exe",
            "RobloxStudio.exe",
            "RobloxPlayerLauncher.exe",
        ]
        for executable in executable_names:
            if (directory / executable).exists():
                return Installation(
                    name="Roblox Studio",
                    path=str(directory),
                    version=directory.name,
                    executable=executable,
                )
        if (directory / "Versions").exists():
            return Installation(
                name="Roblox Studio",
                path=str(directory),
                version=directory.name,
                executable=None,
            )
        return None

    def get_primary_installation(self) -> Installation | None:
        configured = self.config.data.studio_install_path
        if configured:
            path = Path(configured)
            installation = self._inspect_directory(path)
            if installation:
                return installation

        installations = self.detect_installations()
        return installations[0] if installations else None

    def validate_installation(self, path: str) -> bool:
        installation = self._inspect_directory(Path(path))
        return bool(installation and installation.is_valid())

    def open_installation(self, path: str) -> bool:
        installation = self._inspect_directory(Path(path))
        if not installation or not installation.is_valid():
            return False
        executable = installation.executable
        target = Path(path) / executable if executable else Path(path)
        try:
            if os.name == "nt":
                subprocess.Popen([str(target)])
            else:
                subprocess.Popen(["open", str(target)]) if sys_platform == "darwin" else subprocess.Popen([str(target)])
            return True
        except OSError:
            return False


# This is kept to support a portable launch strategy on non-Windows systems.
# The library intentionally avoids shelling out to an unsupported Roblox runtime.
sys_platform = os.name
