from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.i18n import get_translation as t

def create_language_keyboard(lang_code: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t(lang_code, "language_button_russian", "🇷🇺 Русский"), callback_data="lang:ru"),
            InlineKeyboardButton(text=t(lang_code, "language_button_uzbek", "🇺🇿 O'zbekcha"), callback_data="lang:uz"),
            InlineKeyboardButton(text=t(lang_code, "language_button_english", "🇬🇧 English"), callback_data="lang:en"),
        ],
    ])
