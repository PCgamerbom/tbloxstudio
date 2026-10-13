from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FastFlag:
    name: str
    enabled: bool
    description: str = ""


class FastFlagManager:
    DEFAULT_FLAGS = {
        "DFFlagDebugGraphicsEnable": FastFlag(
            "DFFlagDebugGraphicsEnable",
            False,
            "Allows Studio debug graphics in developer builds.",
        ),
        "DFFlagFixGraphicsQuality": FastFlag(
            "DFFlagFixGraphicsQuality",
            True,
            "Keeps frame quality defaults stable while testing.",
        ),
        "DFIntTaskSchedulerTargetFrameRate": FastFlag(
            "DFIntTaskSchedulerTargetFrameRate",
            True,
            "Targets a steady frame rate when the app is open.",
        ),
        "DFIntUseFastFlag": FastFlag(
            "DFIntUseFastFlag",
            True,
            "Enables the active fast flag set for Studio.",
        ),
    }

    def __init__(self, config) -> None:
        self.config = config
        self._flags = self._load_flags()

    def _load_flags(self) -> dict[str, FastFlag]:
        stored_flags = self.config.data.fast_flags or {}
        merged: dict[str, FastFlag] = {}
        for name, flag in self.DEFAULT_FLAGS.items():
            merged[name] = FastFlag(
                name=name,
                enabled=stored_flags.get(name, flag.enabled),
                description=flag.description,
            )
        return merged

    def list_flags(self) -> list[FastFlag]:
        return list(self._flags.values())

    def enabled_flags(self) -> list[FastFlag]:
        return [flag for flag in self._flags.values() if flag.enabled]

    def toggle(self, name: str) -> FastFlag:
        if name not in self._flags:
            raise KeyError(f"Unknown FastFlag: {name}")
        flag = self._flags[name]
        flag.enabled = not flag.enabled
        self.persist()
        return flag

    def set_flag(self, name: str, enabled: bool) -> FastFlag:
        if name not in self._flags:
            raise KeyError(f"Unknown FastFlag: {name}")
        self._flags[name].enabled = enabled
        self.persist()
        return self._flags[name]

    def persist(self) -> None:
        stored = {name: flag.enabled for name, flag in self._flags.items()}
        self.config.set_fast_flags(stored)

    @property
    def count(self) -> int:
        return len(self.enabled_flags())
