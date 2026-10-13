# Modifystrap

Modifystrap is a desktop management application for Roblox Studio installations and customization profiles. It is designed to help users organize Studio installs, track active FastFlags, create profile-based customizations, back up critical files, and keep a simple activity log.

This project is inspired by the original Roblox Studio Mod Manager by MaximumADHD and uses it as a technical reference. It intentionally preserves the original project's licensing context and gives proper attribution without reusing protected assets or code.

## Project goals

- Detect and validate Roblox Studio installation folders.
- Manage multiple installation candidates safely.
- Toggle FastFlags and keep profile-specific state.
- Create backups of installation directories.
- Keep a working activity log for operations and errors.
- Provide a clean desktop UI with a modular Python architecture.

## Architecture

The application is organized into clear modules:

- `modifystrap.config`: persistent app settings, profile metadata, and storage paths.
- `modifystrap.installations`: installation discovery, validation, and launch helpers.
- `modifystrap.fastflags`: flag definitions and per-profile toggle logic.
- `modifystrap.profiles`: profile creation and switching.
- `modifystrap.backups`: zip-based backup and restore workflows.
- `modifystrap.activity`: event logging and recent activity queries.
- `modifystrap.app`: desktop UI built using Tkinter.

## Running the app

```bash
python -m modifystrap
```

## Installing in editable mode

```bash
python -m pip install -e .
```

## Running tests

```bash
pytest
```

## Notes on compatibility

This project is intentionally written to support a Windows-focused workflow while remaining portable enough to execute in a development environment. It does not attempt to replace or bundle the full Roblox Studio runtime; it manages the installation path and configuration state around a real Studio executable when available.

## Credits

- Original reference project: MaximumADHD / Roblox Studio Mod Manager
- License: MIT
