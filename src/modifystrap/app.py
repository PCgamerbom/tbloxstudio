from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .activity import ActivityLog
from .backups import BackupManager
from .config import ConfigStore
from .fastflags import FastFlagManager
from .installations import InstallationManager
from .profiles import ProfileManager


class ModifystrapApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Modifystrap")
        self.geometry("1200x760")
        self.minsize(980, 620)
        self.configure(bg="#0f172a")

        self.config = ConfigStore()
        self.installation_manager = InstallationManager(self.config)
        self.profile_manager = ProfileManager(self.config)
        self.fastflag_manager = FastFlagManager(self.config)
        self.backup_manager = BackupManager(self.config.backups_dir)
        self.activity_log = ActivityLog(self.config)

        self._page_lookup: dict[str, ttk.Frame] = {}
        self._build_theme()
        self._build_sidebar()
        self._build_pages()
        self.show_page("dashboard")

    def _build_theme(self) -> None:
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Sidebar.TFrame", background="#111827")
        self.style.configure("Card.TFrame", background="#111827")
        self.style.configure("Content.TFrame", background="#0f172a")
        self.style.configure("Title.TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 16, "bold"))
        self.style.configure("Body.TLabel", background="#0f172a", foreground="#cbd5e1", font=("Segoe UI", 10))
        self.style.configure("Accent.TButton", background="#38bdf8", foreground="#020617", font=("Segoe UI", 10, "bold"))

    def _build_sidebar(self) -> None:
        self.sidebar = ttk.Frame(self, style="Sidebar.TFrame", width=220)
        self.sidebar.pack_propagate(False)
        self.sidebar.pack(side="left", fill="y")

        title = ttk.Label(self.sidebar, text="Modifystrap", style="Title.TLabel")
        title.pack(anchor="w", padx=18, pady=(18, 12))

        self.nav_buttons = {}
        for name, label in [
            ("dashboard", "Dashboard"),
            ("installations", "Installations"),
            ("fastflags", "FastFlags"),
            ("mods", "Mods & Customizations"),
            ("profiles", "Profiles"),
            ("backups", "Backups"),
            ("activity", "Activity"),
            ("settings", "Settings"),
            ("about", "About & Credits"),
        ]:
            button = ttk.Button(self.sidebar, text=label, command=lambda page=name: self.show_page(page))
            button.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[name] = button

    def _build_pages(self) -> None:
        self.main = ttk.Frame(self, style="Content.TFrame")
        self.main.pack(side="right", fill="both", expand=True)

        self._page_lookup = {}
        for name in [
            "dashboard",
            "installations",
            "fastflags",
            "mods",
            "profiles",
            "backups",
            "activity",
            "settings",
            "about",
        ]:
            frame = ttk.Frame(self.main, style="Content.TFrame")
            frame.pack(fill="both", expand=True)
            self._page_lookup[name] = frame

        self._render_dashboard()
        self._render_installations()
        self._render_fastflags()
        self._render_mods()
        self._render_profiles()
        self._render_backups()
        self._render_activity()
        self._render_settings()
        self._render_about()

    def show_page(self, page_name: str) -> None:
        for name, frame in self._page_lookup.items():
            frame.pack_forget()
        self._page_lookup[page_name].pack(fill="both", expand=True)

    def _card(self, parent: tk.Misc, title: str, value: str, accent: str = "#38bdf8") -> None:
        card = ttk.Frame(parent, padding=(16, 12))
        card.pack(fill="x", expand=True, padx=8, pady=8)
        label = ttk.Label(card, text=title, foreground="#94a3b8", font=("Segoe UI", 10))
        label.pack(anchor="w")
        value_label = ttk.Label(card, text=value, foreground="#f8fafc", font=("Segoe UI", 18, "bold"))
        value_label.pack(anchor="w", pady=(6, 0))
        return card

    def _render_dashboard(self) -> None:
        frame = self._page_lookup["dashboard"]
        frame.configure(style="Content.TFrame")

        header = ttk.Label(frame, text="Dashboard", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))

        cards = ttk.Frame(frame)
        cards.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        installation = self.installation_manager.get_primary_installation()
        installation_status = installation.version if installation else "Not detected"
        active_profile = self.profile_manager.get_active_profile().get("name", "Default")
        enabled_mods = self.fastflag_manager.count
        backup_count = len(self.backup_manager.list_backups())
        recent_activity = self.activity_log.recent(1)

        self._card(cards, "Detected installation", installation_status)
        self._card(cards, "Studio version", installation.version if installation else "Unavailable")
        self._card(cards, "Active profile", str(active_profile))
        self._card(cards, "Enabled modifications", str(enabled_mods))
        self._card(cards, "Backups", str(backup_count))
        self._card(cards, "Latest activity", recent_activity[0]["message"] if recent_activity else "No activity yet")

        actions = ttk.Frame(frame)
        actions.pack(fill="x", padx=18, pady=(0, 18))
        ttk.Button(actions, text="Open Roblox Studio", command=self._open_studio).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Manage FastFlags", command=lambda: self.show_page("fastflags")).pack(side="left", padx=8)
        ttk.Button(actions, text="Review Backups", command=lambda: self.show_page("backups")).pack(side="left", padx=8)

    def _render_installations(self) -> None:
        frame = self._page_lookup["installations"]
        for child in frame.winfo_children():
            child.destroy()

        header = ttk.Label(frame, text="Installations", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))

        installations = self.installation_manager.detect_installations()
        if not installations:
            info = ttk.Label(frame, text="No compatible Roblox Studio installation was detected. Set a path manually in Settings.")
            info.pack(anchor="w", padx=18, pady=12)
            return

        for installation in installations:
            row = ttk.Frame(frame, padding=(18, 10))
            row.pack(fill="x", padx=18, pady=6)
            ttk.Label(row, text=f"{installation.name} — {installation.version}", foreground="#f8fafc", font=("Segoe UI", 12, "bold")).pack(anchor="w")
            ttk.Label(row, text=installation.path, foreground="#94a3b8").pack(anchor="w")
            ttk.Button(row, text="Open", command=lambda path=installation.path: self._open_studio_path(path)).pack(anchor="w", pady=(8, 0))

    def _render_fastflags(self) -> None:
        frame = self._page_lookup["fastflags"]
        for child in frame.winfo_children():
            child.destroy()

        header = ttk.Label(frame, text="FastFlags", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))

        for flag in self.fastflag_manager.list_flags():
            row = ttk.Frame(frame, padding=(18, 8))
            row.pack(fill="x", padx=18, pady=4)
            label = ttk.Label(row, text=flag.name, foreground="#f8fafc", font=("Segoe UI", 10, "bold"))
            label.pack(anchor="w")
            ttk.Label(row, text=flag.description, foreground="#94a3b8").pack(anchor="w")
            var = tk.BooleanVar(value=flag.enabled)
            check = ttk.Checkbutton(row, text="Enabled" if flag.enabled else "Disabled", variable=var, command=lambda name=flag.name, var=var: self._toggle_fastflag(name, var))
            check.pack(anchor="w", pady=(6, 0))

    def _render_mods(self) -> None:
        frame = self._page_lookup["mods"]
        for child in frame.winfo_children():
            child.destroy()
        header = ttk.Label(frame, text="Mods & Customizations", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))
        ttk.Label(frame, text="Theme overrides, Studio patches, and external resource integrations are organized here.", foreground="#94a3b8").pack(anchor="w", padx=18)

    def _render_profiles(self) -> None:
        frame = self._page_lookup["profiles"]
        for child in frame.winfo_children():
            child.destroy()
        header = ttk.Label(frame, text="Profiles", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))

        profiles = self.profile_manager.list_profiles()
        for profile in profiles:
            row = ttk.Frame(frame, padding=(18, 10))
            row.pack(fill="x", padx=18, pady=6)
            ttk.Label(row, text=profile.get("name", "Profile"), foreground="#f8fafc", font=("Segoe UI", 12, "bold")).pack(anchor="w")
            ttk.Button(row, text="Activate", command=lambda profile_name=profile.get("name"): self._activate_profile(profile_name)).pack(anchor="w", pady=(8, 0))

        ttk.Button(frame, text="Create profile", command=self._create_profile).pack(anchor="w", padx=18, pady=(18, 0))

    def _render_backups(self) -> None:
        frame = self._page_lookup["backups"]
        for child in frame.winfo_children():
            child.destroy()
        header = ttk.Label(frame, text="Backups", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))

        backups = self.backup_manager.list_backups()
        if not backups:
            ttk.Label(frame, text="No backups have been created yet.", foreground="#94a3b8").pack(anchor="w", padx=18)
            return

        for archive in backups:
            row = ttk.Frame(frame, padding=(18, 10))
            row.pack(fill="x", padx=18, pady=6)
            ttk.Label(row, text=archive.name, foreground="#f8fafc").pack(anchor="w")
            ttk.Button(row, text="Restore", command=lambda path=str(archive): self._restore_backup(path)).pack(anchor="w", pady=(8, 0))

    def _render_activity(self) -> None:
        frame = self._page_lookup["activity"]
        for child in frame.winfo_children():
            child.destroy()
        header = ttk.Label(frame, text="Activity", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))

        for item in self.activity_log.recent():
            row = ttk.Frame(frame, padding=(18, 8))
            row.pack(fill="x", padx=18, pady=4)
            ttk.Label(row, text=item.get("timestamp", ""), foreground="#94a3b8").pack(anchor="w")
            ttk.Label(row, text=item.get("message", ""), foreground="#f8fafc").pack(anchor="w")

    def _render_settings(self) -> None:
        frame = self._page_lookup["settings"]
        for child in frame.winfo_children():
            child.destroy()
        header = ttk.Label(frame, text="Settings", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))

        ttk.Label(frame, text="Studio install path", foreground="#cbd5e1").pack(anchor="w", padx=18)
        path_var = tk.StringVar(value=self.config.data.studio_install_path or "")
        entry = ttk.Entry(frame, textvariable=path_var, width=80)
        entry.pack(fill="x", padx=18, pady=(4, 12))
        ttk.Button(frame, text="Save install path", command=lambda: self._save_install_path(path_var.get())).pack(anchor="w", padx=18)

    def _render_about(self) -> None:
        frame = self._page_lookup["about"]
        for child in frame.winfo_children():
            child.destroy()
        header = ttk.Label(frame, text="About & Credits", font=("Segoe UI", 24, "bold"), foreground="#e2e8f0")
        header.pack(anchor="w", padx=18, pady=(18, 12))
        ttk.Label(frame, text="Modifystrap is a premium desktop manager for Roblox Studio installs, profiles, backups, and active configuration.", foreground="#cbd5e1", wraplength=700, justify="left").pack(anchor="w", padx=18, pady=(0, 10))
        ttk.Label(frame, text="Reference project: MaximumADHD / Roblox Studio Mod Manager (MIT)\nProject approach: portable Python desktop management for Studio workflows.", foreground="#94a3b8", wraplength=700, justify="left").pack(anchor="w", padx=18)

    def _toggle_fastflag(self, name: str, var: tk.BooleanVar) -> None:
        enabled = bool(var.get())
        self.fastflag_manager.set_flag(name, enabled)
        self.activity_log.record(f"FastFlag {name} set to {enabled}")
        self._refresh_all_frames()

    def _activate_profile(self, profile_name: str) -> None:
        profile = self.profile_manager.switch_profile(profile_name)
        self.activity_log.record(f"Activated profile: {profile.get('name')}")
        self._refresh_all_frames()

    def _create_profile(self) -> None:
        name = simple_input("Profile name", "Create a new profile")
        if not name:
            return
        try:
            self.profile_manager.create_profile(name)
            self.activity_log.record(f"Created profile: {name}")
            self._refresh_all_frames()
        except ValueError as exc:
            messagebox.showerror("Profile error", str(exc))

    def _save_install_path(self, path: str) -> None:
        cleaned = path.strip()
        self.config.data.studio_install_path = cleaned or None
        self.config.save(self.config.data)
        self.activity_log.record(f"Saved install path: {cleaned or 'None'}")
        self._refresh_all_frames()

    def _restore_backup(self, archive_path: str) -> None:
        try:
            destination = self.backup_manager.restore_backup(archive_path, self.config.root_dir / "restore")
            self.activity_log.record(f"Restored backup {archive_path} into {destination}")
            messagebox.showinfo("Backup restored", f"Files restored to {destination}")
        except Exception as exc:  # pragma: no cover - UI only
            messagebox.showerror("Restore failed", str(exc))

    def _open_studio(self) -> None:
        installation = self.installation_manager.get_primary_installation()
        if not installation:
            messagebox.showwarning("No installation", "No Roblox Studio installation could be found.")
            return
        if not self.installation_manager.open_installation(installation.path):
            messagebox.showerror("Launch failed", "Roblox Studio could not be launched from the detected install.")
            return
        self.activity_log.record(f"Launched Studio {installation.path}")

    def _open_studio_path(self, path: str) -> None:
        if not self.installation_manager.open_installation(path):
            messagebox.showerror("Launch failed", "Roblox Studio could not be launched.")
            return
        self.activity_log.record(f"Launched Studio from custom path: {path}")

    def _refresh_all_frames(self) -> None:
        self._render_dashboard()
        self._render_installations()
        self._render_fastflags()
        self._render_mods()
        self._render_profiles()
        self._render_backups()
        self._render_activity()
        self._render_settings()
        self._render_about()


def simple_input(title: str, prompt: str) -> str:
    root = tk.Tk()
    root.withdraw()
    value = simpledialog = None
    try:
        import tkinter.simpledialog as simpledialog
        value = simpledialog.askstring(title, prompt)
    finally:
        root.destroy()
    return value or ""


def main() -> None:
    app = ModifystrapApp()
    app.mainloop()
