from __future__ import annotations

import os

from .config import ConfigStore


def main() -> None:
    if os.environ.get("DISPLAY", "") == "" and os.name != "nt":
        config = ConfigStore()
        print("Modifystrap is running in headless mode.")
        print(f"Active profile: {config.data.active_profile}")
        print(f"Studio install path: {config.data.studio_install_path or 'not configured'}")
        return

    from .app import ModifystrapApp

    app = ModifystrapApp()
    app.mainloop()


if __name__ == "__main__":
    main()
