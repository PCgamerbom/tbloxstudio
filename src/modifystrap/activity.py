from __future__ import annotations

from datetime import datetime, timezone


class ActivityLog:
    def __init__(self, config) -> None:
        self.config = config

    def record(self, message: str, level: str = "info") -> None:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        item = {"timestamp": timestamp, "message": message, "level": level}
        activities = list(self.config.get_recent_activities())
        activities.append(item)
        if len(activities) > 25:
            activities = activities[-25:]
        self.config.data.recent_activities = activities
        self.config.save(self.config.data)

    def recent(self, count: int = 5) -> list[dict[str, str]]:
        activities = self.config.get_recent_activities()
        return activities[-count:] if count else activities
