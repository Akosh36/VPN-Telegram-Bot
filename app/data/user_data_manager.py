import json
import os
import logging
from typing import Dict, Any
from pathlib import Path # Import Path for type hinting

from app.config import USERS_FILE_PATH

logger = logging.getLogger(__name__)

class UserDataManager:
    def __init__(self, file_path: Path = USERS_FILE_PATH):
        self.file_path = file_path
        self._users_data: Dict[str, Any] = self._load_users_data()

    def _load_users_data(self) -> Dict[str, Any]:
        """Loads user data from the users.json file."""
        logger.info(f"Attempting to load user data from {self.file_path}.")
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    logger.info(f"Successfully loaded user data from {self.file_path}.")
                    return data
            except json.JSONDecodeError:
                logger.warning(
                    f"Error decoding JSON from {self.file_path}. Returning empty data."
                )
                return {}
        else:
            logger.info(f"{self.file_path} not found. Returning empty user data.")
            return {}

    def save_users_data(self) -> None:
        """Saves user data to the users.json file."""
        logger.info(f"Attempting to save user data to {self.file_path}.")
        try:
            with open(self.file_path, "w") as f:
                json.dump(self._users_data, f, indent=4)
            logger.info(f"Successfully saved user data to {self.file_path}.")
        except IOError as e:
            logger.error(f"Error saving user data to {self.file_path}: {e}")

    def get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Returns data for a specific user."""
        return self._users_data.get(user_id, {})

    def update_user_data(self, user_id: str, data: Dict[str, Any]) -> None:
        """Updates data for a specific user and saves to file."""
        if user_id not in self._users_data:
            self._users_data[user_id] = {}
        self._users_data[user_id].update(data)
        self.save_users_data()

    def get_all_users_data(self) -> Dict[str, Any]:
        """Returns all users data."""
        return self._users_data

    def get_lang(self, user_id: str, default: str = "en") -> str:
        """Return user's language code, defaulting to 'en'."""
        user = self._users_data.get(user_id, {})
        return user.get("lang", default)

    def set_lang(self, user_id: str, lang_code: str) -> None:
        """Set user's language code and persist."""
        if user_id not in self._users_data:
            self._users_data[user_id] = {}
        self._users_data[user_id]["lang"] = lang_code
        self.save_users_data()
