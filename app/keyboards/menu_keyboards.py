from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from app.utils.i18n import get_translation as t


def create_main_menu_keyboard(lang_code: str = "en") -> ReplyKeyboardMarkup:
    """Define a function to create the main menu keyboard."""
    menu_buttons = [
        [KeyboardButton(text=t(lang_code, "main_menu_button_tariflar")), KeyboardButton(text=t(lang_code, "main_menu_button_kalitlarim"))],
        [KeyboardButton(text=t(lang_code, "main_menu_button_accauntim")), KeyboardButton(text=t(lang_code, "main_menu_button_korsatmalar"))],
        [KeyboardButton(text=t(lang_code, "main_menu_button_yordam")), KeyboardButton(text=t(lang_code, "main_menu_button_dustim"))],
    ]
    return ReplyKeyboardMarkup(
        keyboard=menu_buttons, resize_keyboard=True, one_time_keyboard=False
    )


def create_server_location_keyboard(lang_code: str = "en") -> InlineKeyboardMarkup:
    """Creates an Inline Keyboard Markup for server location selection."""
    server_buttons = [
        [InlineKeyboardButton(text=t(lang_code, "server_button_russia"), callback_data="select_server_russia")],
        [InlineKeyboardButton(text=t(lang_code, "server_button_america"), callback_data="select_server_america")],
        [InlineKeyboardButton(text=t(lang_code, "server_button_germany"), callback_data="select_server_germany")],
        [
            InlineKeyboardButton(
                text=t(lang_code, "server_button_singapore"), callback_data="select_server_singapore"
            )
        ],
        [InlineKeyboardButton(text=t(lang_code, "button_back_to_main"), callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=server_buttons)


def create_accauntim_keyboard(lang_code: str = "en") -> InlineKeyboardMarkup:
    """Creates an Inline Keyboard Markup for the Accauntim menu."""
    accauntim_buttons = [
        [InlineKeyboardButton(text=t(lang_code, "button_enter_promo_code"), callback_data="enter_promo_code")],
        [InlineKeyboardButton(text=t(lang_code, "button_back_to_main"), callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=accauntim_buttons)
