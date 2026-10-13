from __future__ import annotations

import shutil
import zipfile
from datetime import datetime
from pathlib import Path


class BackupManager:
    def __init__(self, backups_dir: str | Path) -> None:
        self.backups_dir = Path(backups_dir)
        self.backups_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, source_dir: str | Path, label: str = "manual") -> Path:
        source = Path(source_dir)
        if not source.exists():
            raise FileNotFoundError(f"Source directory does not exist: {source}")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        archive_name = f"{label}-{timestamp}.zip"
        archive_path = self.backups_dir / archive_name

        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in sorted(source.rglob("*")):
                if file_path.is_file():
                    archive.write(file_path, file_path.relative_to(source))

        return archive_path

    def list_backups(self) -> list[Path]:
        return sorted(self.backups_dir.glob("*.zip"), key=lambda item: item.name)

    def restore_backup(self, archive_path: str | Path, destination_dir: str | Path) -> Path:
        source = Path(archive_path)
        if not source.exists():
            raise FileNotFoundError(f"Backup archive not found: {source}")

        destination = Path(destination_dir)
        destination.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(source, "r") as archive:
            archive.extractall(destination)

        return destination

    def delete_backup(self, archive_path: str | Path) -> None:
        path = Path(archive_path)
        if path.exists():
            path.unlink()
