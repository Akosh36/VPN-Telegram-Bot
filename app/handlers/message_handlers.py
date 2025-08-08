import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.utils.i18n import get_translation as t
from app.utils.markdown_utils import escape_markdown_v2 # NEW: Import markdown escape utility
from app.keyboards.language_keyboards import create_language_keyboard
from app.keyboards.menu_keyboards import create_main_menu_keyboard, create_server_location_keyboard, create_accauntim_keyboard
from app.data.user_data_manager import UserDataManager

logger = logging.getLogger(__name__)

def register_message_handlers(router: Router, user_data_manager: UserDataManager):
    @router.message(Command("start"))
    async def cmd_start(message: Message):
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id) # Get user's preferred language

        logger.info(f"Received /start from {user_id} with lang={lang}")
        await message.answer(
            t(lang, "welcome_message", "Hello! Welcome to our bot!"),
            reply_markup=create_main_menu_keyboard(lang),
        )
        # Always offer language selection after the main menu
        await message.answer(
            t(lang, "language_selection_prompt", "Please select a language:"),
            reply_markup=create_language_keyboard(lang),
        )

    # Allow users to change language explicitly (now redundant but can be kept)
    @router.message(Command("language"))
    async def cmd_language(message: Message):
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        await message.answer(
            t(lang, "language_selection_prompt", "Please select a language:"),
            reply_markup=create_language_keyboard(lang),
        )

    # Handle language selection via inline keyboard: callback_data like "lang:ru"
    @router.callback_query(F.data.startswith("lang:"))
    async def on_language_selected(callback: CallbackQuery):
        user_id = str(callback.from_user.id)
        _, lang_code = callback.data.split(":", 1)

        # Save language
        user_data_manager.set_lang(user_id, lang_code)
        logger.info(f"Language set to {lang_code} for user {user_id}")

        # Confirm to the user and update messages in selected language
        await callback.message.edit_text(
            t(lang_code, "language_set_confirmation", "Language has been set. Main menu:") # New key for confirmation
        )
        # Update the main menu keyboard
        await callback.message.answer(
            t(lang_code, "welcome_message", "Hello! Welcome to our bot!"), # Re-send welcome for consistency
            reply_markup=create_main_menu_keyboard(lang_code),
        )
        await callback.answer()

    @router.message(
        F.text.in_([
            t("ru", "main_menu_button_tariflar"),
            t("uz", "main_menu_button_tariflar"),
            t("en", "main_menu_button_tariflar")
        ])
    )
    async def handle_tariflar(message: Message):
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(f"Received '💎 Tariflar' from user {user_id}")
        await message.answer(
            t(lang, "server_selection_prompt", "Please select a server location:"),
            reply_markup=create_server_location_keyboard(lang),
        )
        logger.info(f"Sent server selection menu to user {user_id}")


    @router.message(
        F.text.in_([
            t("ru", "main_menu_button_kalitlarim"),
            t("uz", "main_menu_button_kalitlarim"),
            t("en", "main_menu_button_kalitlarim")
        ])
    )
    async def handle_kalitlarim(message: Message):
        """
        Handles the "🔑 Kalitlarim" button press and displays the user's generated keys.
        """
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(f"Received '🔑 Kalitlarim' from user {user_id}")
        user_data = user_data_manager.get_user_data(user_id)

        if user_data and user_data.get("keys"):
            user_keys = user_data["keys"]
            if user_keys:
                logger.info(f"Displaying {len(user_keys)} keys for user {user_id}.")
                # Format the keys into a readable message
                keys_message_raw = t(lang, "keys_message_header", "Your saved keys:") + "\n\n"
                for i, key in enumerate(user_keys):
                    # Escape the dot in the number and any special characters in the key
                    escaped_key = escape_markdown_v2(key) # Use the new escape utility
                    keys_message_raw += f"{i + 1}\\. `{escaped_key}`\n\n"

                await message.answer(keys_message_raw, parse_mode="MarkdownV2")
            else:
                logger.info(f"User {user_id} has no saved keys.")
                await message.answer(t(lang, "no_saved_keys", "You don't have any saved keys yet."))
        else:
            logger.info(f"User {user_id} has no saved keys in database.")
            await message.answer(t(lang, "no_saved_keys", "You don't have any saved keys yet."))

        # Display the main menu again
        await message.answer(t(lang, "main_menu_message_prompt", "Main menu:"), reply_markup=create_main_menu_keyboard(lang)) # New key
        logger.info(f"Sent main menu to user {user_id}")


    @router.message(
        F.text.in_([
            t("ru", "main_menu_button_accauntim"),
            t("uz", "main_menu_button_accauntim"),
            t("en", "main_menu_button_accauntim")
        ])
    )
    async def handle_accauntim(message: Message):
        """
        Handles the "👤 Accauntim" button press and displays user account info
        with an inline keyboard for promo code entry.
        """
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(f"Received '👤 Accauntim' from user {user_id}")
        account_info_raw = f"{t(lang, 'account_info_header', 'Your Account:')}\n\n{t(lang, 'account_info_user_id', 'User ID:')} `{escape_markdown_v2(user_id)}`"

        await message.answer(
            account_info_raw, reply_markup=create_accauntim_keyboard(lang), parse_mode="MarkdownV2" # Pass lang
        )
        logger.info(f"Sent account info and inline keyboard to user {user_id}")


    @router.message(
        F.text.in_([
            t("ru", "main_menu_button_korsatmalar"),
            t("uz", "main_menu_button_korsatmalar"),
            t("en", "main_menu_button_korsatmalar")
        ])
    )
    async def handle_korsatmalar(message: Message):
        """
        Handles the "📘 Ko'rsatmalar" button press and displays installation instructions.
        """
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(f"Received '📘 Ko'rsatmalar' from user {user_id}")
        # Instructions text can be put in translation files if they vary by language
        instructions_text = t(lang, "instructions_full_text", """
<b>📘 Instructions</b>

<b>For Android:</b>
1. Download V2RayNG from Google Play Store.
2. Copy your VPN link above.
3. Open the app and tap the "+" button in the top right corner.
4. Select "Import config from Clipboard".
5. Tap the round button in the bottom right corner to start the connection.

<b>For Windows:</b>
1. Download either V2RayN or Qv2ray.
2. Install and launch the application.
3. Copy your VPN link.
4. Find the 'Import' or 'Add' button in the app and paste the link.
5. Activate the connection.

<b>For iPhone:</b>
1. Download Shadowrocket, V2RayNG (if available), or another V2Ray/Xray client from the App Store.
2. Open the app.
3. Copy your VPN link.
4. Find the 'Add Server' or similar button in the app and import the link.
5. Start the connection.

<b>For Mac:</b>
1. Download V2RayX, Qv2ray, or another compatible client app.
2. Install and open the app.
3. Copy your VPN link.
4. Find the 'Import' or 'Add' button in the app and paste the link.
5. Activate the connection.
""")
        await message.answer(instructions_text, parse_mode="HTML") # Instructions text is fixed for now
        logger.info(f"Sent instructions to user {user_id}")

        # Display the main menu again
        await message.answer(t(lang, "main_menu_message_prompt", "Main menu:"), reply_markup=create_main_menu_keyboard(lang))
        logger.info(f"Sent main menu to user {user_id}")


    @router.message(
        F.text.in_([
            t("ru", "main_menu_button_yordam"),
            t("uz", "main_menu_button_yordam"),
            t("en", "main_menu_button_yordam")
        ])
    )
    async def handle_yordam(message: Message):
        """
        Handles the "🆘 Yordam" button press and displays help information.
        """
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(f"Received '🆘 Yordam' from user {user_id}")
        # Help text can be put in translation files if they vary by language
        help_text = t(lang, "help_full_text", """
<b>🆘 Help</b>

<b>Common problems and solutions:</b>

<b>1. VPN is not working:</b>
- Check your internet connection.
- Make sure you copied the VPN link correctly.
- Try re-selecting the server in your application.
- If the problem persists, try generating a new key ("💎 Tariffs").

<b>2. Slow internet:</b>
- Try selecting a different server location ("💎 Tariffs"). Some servers may be closer to your location.
- Contact your internet provider to check the overall internet speed.

<b>3. Bot is not working:</b>
- Try again after a few minutes. The bot may be undergoing technical maintenance.
- If the problem persists, use the contact information in the "👥 My Friend" menu (if available) to contact the administrator.
""")
        await message.answer(help_text, parse_mode="HTML") # Help text is fixed for now
        logger.info(f"Sent help information to user {user_id}")

        # Display the main menu again
        await message.answer(t(lang, "main_menu_message_prompt", "Main menu:"), reply_markup=create_main_menu_keyboard(lang))
        logger.info(f"Sent main menu to user {user_id}")


    @router.message(
        F.text.in_([
            t("ru", "main_menu_button_dustim"),
            t("uz", "main_menu_button_dustim"),
            t("en", "main_menu_button_dustim")
        ])
    )
    async def handle_dustim(message: Message):
        """
        Handles the "👥 Do'stim" button press, shows a referral link,
        and a placeholder message about referral tracking.
        """
        user_id = str(message.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(f"Received '👥 Do'stim' from user {user_id}")
        bot_username = "your_bot_username"  # IMPORTANT: Replace with your actual bot username (e.g., "my_awesome_vpn_bot")
        referral_link = f"https://t.me/{bot_username}?start={user_id}"

        # Escape special characters for MarkdownV2
        escaped_link = escape_markdown_v2(referral_link) # Use the new escape utility
        referral_bonus_info_escaped = escape_markdown_v2(t(lang, "referral_bonus_info", "Invite your friends and get bonuses! (Referral accounting is basic for now)"))

        referral_message = f"""
{t(lang, "referral_link_message", "Your referral link:")}
`{escaped_link}`

{referral_bonus_info_escaped}
"""
        await message.answer(referral_message, parse_mode="MarkdownV2")
        logger.info(f"Sent referral link to user {user_id}")

        # Display the main menu again
        await message.answer(t(lang, "main_menu_message_prompt", "Main menu:"), reply_markup=create_main_menu_keyboard(lang))
        logger.info(f"Sent main menu to user {user_id}")
