"""
Configuration module for the Telegram VPN bot.
This centralizes environment-driven settings so that future refactoring
can import from a single place. For now, this file is not wired into the
legacy main.py to avoid breaking changes, but new modules should import
from here.
"""

from __future__ import annotations

import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# Base directories
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
VAR_DIR: Path = PROJECT_ROOT / "var"
VAR_DIR.mkdir(parents=True, exist_ok=True)

# Telegram Bot settings
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()

# Data files
USERS_FILE_NAME: str = os.getenv("USERS_FILE", "users.json")
USERS_FILE_PATH: Path = VAR_DIR / USERS_FILE_NAME

# Feature flags / misc
DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes", "y")

__all__ = [
    "PROJECT_ROOT",
    "VAR_DIR",
    "BOT_TOKEN",
    "USERS_FILE_NAME",
    "USERS_FILE_PATH",
    "DEBUG",
    "logger", # Added logger to __all__
]
