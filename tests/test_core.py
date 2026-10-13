from __future__ import annotations

from pathlib import Path

from modifystrap.backups import BackupManager
from modifystrap.config import ConfigStore
from modifystrap.fastflags import FastFlagManager
from modifystrap.installations import InstallationManager
from modifystrap.profiles import ProfileManager


def test_config_store_round_trip(tmp_path):
    config = ConfigStore(root_dir=tmp_path)
    assert config.data.theme == "dark"
    config.update(theme="light")
    assert config.data.theme == "light"


def test_fastflag_toggle(tmp_path):
    config = ConfigStore(root_dir=tmp_path)
    manager = FastFlagManager(config)
    flag = manager.toggle("DFFlagDebugGraphicsEnable")
    assert flag.enabled is True
    assert manager.enabled_flags()[0].name == "DFFlagDebugGraphicsEnable"


def test_profile_manager_switches_profile(tmp_path):
    config = ConfigStore(root_dir=tmp_path)
    manager = ProfileManager(config)
    manager.create_profile("Testing")
    manager.switch_profile("Testing")
    assert manager.get_active_profile()["name"] == "Testing"


def test_installation_detection(tmp_path):
    install_dir = tmp_path / "RobloxStudioBeta"
    install_dir.mkdir()
    (install_dir / "RobloxStudioBeta.exe").write_text("stub", encoding="utf-8")
    config = ConfigStore(root_dir=tmp_path / "config")
    manager = InstallationManager(config)
    detected = manager.detect_installations()
    assert any(item.path == str(install_dir) for item in detected)


def test_backup_round_trip(tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    file_path = source_dir / "settings.json"
    file_path.write_text('{"mode": "safe"}', encoding="utf-8")

    backup_dir = tmp_path / "backups"
    manager = BackupManager(backup_dir)
    archive = manager.create_backup(source_dir, "sample")
    assert archive.exists()

    restore_target = tmp_path / "restore"
    manager.restore_backup(archive, restore_target)
    assert (restore_target / "settings.json").exists()
