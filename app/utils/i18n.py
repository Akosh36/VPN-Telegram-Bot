import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Base directory for locales
LOCALES_DIR = Path(__file__).parent.parent / "locales"

_translations_cache = {}

def load_translation_file(lang_code: str) -> dict:
    """Loads a translation file into the cache."""
    if lang_code not in _translations_cache:
        file_path = LOCALES_DIR / f"{lang_code}.json"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                _translations_cache[lang_code] = json.load(f)
            logger.info(f"Loaded translation file: {file_path}")
        except FileNotFoundError:
            logger.error(f"Translation file not found: {file_path}")
            _translations_cache[lang_code] = {} # Store empty dict to avoid repeated errors
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from translation file: {file_path}")
            _translations_cache[lang_code] = {}
    return _translations_cache[lang_code]

def get_translation(lang_code: str, key: str, default: str = None) -> str:
    """
    Retrieves a translated string for a given key and language code.
    If the key is not found, returns the default or the key itself.
    """
    translations = load_translation_file(lang_code)
    if key not in translations and default is None:
        logger.warning(f"Translation key '{key}' not found for language '{lang_code}'. Returning key itself.")
        return key
    return translations.get(key, default if default is not None else key)

# Ensure locales directory exists when i18n module is imported
LOCALES_DIR.mkdir(parents=True, exist_ok=True)
