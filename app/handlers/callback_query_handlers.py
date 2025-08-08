import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.keyboards.menu_keyboards import create_main_menu_keyboard
from app.services.vpn_link_generator import VPNLinkGenerator
from app.data.user_data_manager import UserDataManager
from app.utils.i18n import get_translation as t

logger = logging.getLogger(__name__)

def register_callback_query_handlers(
    router: Router,
    user_data_manager: UserDataManager,
    vpn_link_generator: VPNLinkGenerator
):
    @router.callback_query(F.data.startswith("select_server_"))
    async def process_server_selection(callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(
            f"Received server selection callback query '{callback_query.data}' from user {user_id}"
        )
        server_location = callback_query.data.split("_")[-1]  # e.g., 'russia'

        # Placeholder server details (replace with actual server info)
        server_details = {
            "russia": {
                "address": "ru.example.com",
                "port": 443,
                "security": "tls",
                "network": "ws",
                "path": "/ws",
            },
            "america": {
                "address": "us.example.com",
                "port": 8443,
                "security": "tls",
                "network": "tcp",
                "flow": "xtls-rprx-vision",
            },
            "germany": {
                "address": "de.example.com",
                "port": 2053,
                "security": "tls",
                "network": "ws",
                "path": "/v2ray",
            },
            "singapore": {
                "address": "sg.example.com",
                "port": 443,
                "security": "tls",
                "network": "tcp",
            },
        }

        selected_server = server_details.get(server_location)

        if not selected_server:
            logger.warning(
                f"User {user_id} selected unknown server location: {server_location}"
            )
            await callback_query.answer(t(lang, "server_not_found", "Server not found."), show_alert=True)
            return

        # Determine link type (can be dynamic based on server, for now let's assume vmess for ws, vless for tcp with flow)
        link_type = "vmess" if selected_server.get("network") == "ws" else "vless"
        logger.info(f"User {user_id} selected {server_location}. Generating {link_type} link.")

        try:
            # Generate the VPN link
            generated_link = vpn_link_generator.generate_vpn_link(
                link_type,
                selected_server["address"],
                selected_server["port"],
                security=selected_server.get("security", "auto"),
                network=selected_server.get("network", "tcp"),
                **{
                    k: v
                    for k, v in selected_server.items()
                    if k not in ["address", "port", "security", "network"]
                },  # Pass extra args
            )

            # Update user data
            user_data = user_data_manager.get_user_data(user_id)
            if "keys" not in user_data:
                user_data["keys"] = []
            user_data["keys"].append(generated_link)
            user_data_manager.update_user_data(user_id, user_data)
            logger.info(f"Saved new key for user {user_id}.")

            # Send the link to the user
            await callback_query.message.answer(
                f"{t(lang, 'your_vpn_link', 'Your VPN link:')}\n`{generated_link}`", parse_mode="MarkdownV2"
            )
            logger.info(f"Sent VPN link to user {user_id}")

            # Answer the callback query to remove the loading state
            await callback_query.answer(t(lang, "link_generated", "Link generated!"))
            logger.info(f"Answered callback query for user {user_id}")

            # Display the main menu again
            await callback_query.message.answer(
                t(lang, "main_menu_message_prompt", "Main menu:"), reply_markup=create_main_menu_keyboard(lang)
            )
            logger.info(f"Sent main menu to user {user_id}")


        except ValueError as e:
            logger.error(f"ValueError during link generation for user {user_id}: {e}")
            await callback_query.answer(f"{t(lang, 'error_prefix', 'Error:')} {e}", show_alert=True)
        except Exception as e:
            logger.error(
                f"Error generating or saving link for user {user_id}: {e}", exc_info=True
            )  # Log traceback
            await callback_query.answer(t(lang, "error_during_link_generation", "An unexpected error occurred during link generation."), show_alert=True)


    @router.callback_query(F.data == "back_to_main")
    async def process_back_to_main(callback_query: CallbackQuery):
        user_id = str(callback_query.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(
            f"Received 'Back to main' callback query from user {user_id}"
        )
        await callback_query.answer()  # Answer the callback query
        await callback_query.message.answer(
            t(lang, "main_menu_message_prompt", "Main menu:"), reply_markup=create_main_menu_keyboard(lang)
        )
        logger.info(f"Sent main menu to user {user_id}")


    @router.callback_query(F.data == "enter_promo_code")
    async def process_enter_promo_code(callback_query: CallbackQuery):
        """
        Handles the "Promo kod kiritish" callback query and prompts the user for a promo code.
        """
        user_id = str(callback_query.from_user.id)
        lang = user_data_manager.get_lang(user_id)
        logger.info(
            f"Received 'enter_promo_code' callback query from user {user_id}"
        )
        await callback_query.answer()  # Answer the callback query
        # For now, just prompt the user. Promo code logic will be implemented later.
        await callback_query.message.answer(t(lang, "enter_promo_code_prompt", "Please enter your promo code:"))
        logger.info(f"Prompted user {user_id} for promo code.")
