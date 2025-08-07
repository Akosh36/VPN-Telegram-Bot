import os
import logging
import asyncio
import traceback
import json
import uuid
import base64
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.info("Logging configured.")

# Load bot token from .env file
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = "8145315320:AAHCwH2Rujj4-lEN0Ix3FrcuKReL5UYmOMk"  # Fallback token
    logging.warning("Using fallback BOT_TOKEN. Consider setting it in .env file.")
else:
    logging.info("Using BOT_TOKEN from environment variables.")


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.info("Bot and Dispatcher initialized.")

USERS_FILE = "users.json"


def load_users_data():
    """Loads user data from the users.json file."""
    logging.info(f"Attempting to load user data from {USERS_FILE}.")
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                data = json.load(f)
                logging.info(f"Successfully loaded user data from {USERS_FILE}.")
                return data
        except json.JSONDecodeError:
            logging.warning(
                f"Error decoding JSON from {USERS_FILE}. Returning empty data."
            )
            return {}
    else:
        logging.info(f"{USERS_FILE} not found. Returning empty user data.")
        return {}


def save_users_data(users_data):
    """Saves user data to the users.json file."""
    logging.info(f"Attempting to save user data to {USERS_FILE}.")
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users_data, f, indent=4)
        logging.info(f"Successfully saved user data to {USERS_FILE}.")
    except IOError as e:
        logging.error(f"Error saving user data to {USERS_FILE}: {e}")


# Load data when the bot starts
users_data = load_users_data()


def generate_vpn_link(
    link_type, server_address, port, security="auto", network="tcp", **kwargs
):
    """
    Generates a fake or real vmess:// or vless:// link.

    Args:
        link_type (str): The type of the link ('vmess' or 'vless').
        server_address (str): The server address or IP.
        port (int): The server port.
        security (str): The security protocol (e.g., 'auto', 'none', 'tls'). Defaults to 'auto'.
        network (str): The network type (e.g., 'tcp', 'ws'). Defaults to 'tcp'.
        **kwargs: Additional parameters specific to the link type (e.g., 'path' for ws, 'flow' for vless).

    Returns:
        str: The generated VPN link string.

    Raises:
        ValueError: If the link_type is not 'vmess' or 'vless'.
    """
    logging.info(
        f"Generating VPN link of type {link_type} for server {server_address}:{port}"
    )
    user_id = str(uuid.uuid4())

    if link_type.lower() == "vmess":
        vmess_config = {
            "v": "2",
            "ps": "Replit Bot Generated",  # Placeholder name
            "add": server_address,
            "port": str(port),
            "id": user_id,
            "aid": "0",  # AlterId, commonly 0 for single-user links
            "net": network,
            "type": "none",  # Usually 'none' for tcp, or 'ws'
            "host": "",
            "path": "",
            "tls": "",
            "sni": "",
            "alpn": "",
            "scy": security,  # Use the passed security parameter
        }

        # Update with specific kwargs if provided
        vmess_config.update(kwargs)
        logging.debug(f"VMess config: {vmess_config}")

        json_config = json.dumps(vmess_config)
        encoded_config = base64.b64encode(json_config.encode("utf-8")).decode("utf-8")
        link = f"vmess://{encoded_config}"
        logging.info("VMess link generated successfully.")
        return link

    elif link_type.lower() == "vless":
        # Construct VLESS parameters
        params = f"security={security}&type={network}"

        # Add specific kwargs as parameters
        for key, value in kwargs.items():
            params += f"&{key}={value}"

        link = (
            f"vless://{user_id}@{server_address}:{port}?{params}#Replit Bot Generated"
        )  # Placeholder name
        logging.info("VLESS link generated successfully.")
        return link

    else:
        logging.error(f"Invalid link_type specified: {link_type}")
        raise ValueError("Invalid link_type. Must be 'vmess' or 'vless'.")


# Define a function to create the main menu keyboard
def create_main_menu_keyboard():
    menu_buttons = [
        [KeyboardButton(text="💎 Tariflar"), KeyboardButton(text="🔑 Kalitlarim")],
        [KeyboardButton(text="👤 Accauntim"), KeyboardButton(text="📘 Ko'rsatmalar")],
        [KeyboardButton(text="🆘 Yordam"), KeyboardButton(text="👥 Do‘stim")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=menu_buttons, resize_keyboard=True, one_time_keyboard=False
    )


# Define a function to create the server location keyboard
def create_server_location_keyboard():
    """Creates an Inline Keyboard Markup for server location selection."""
    server_buttons = [
        [InlineKeyboardButton(text="🇷🇺 Russia", callback_data="select_server_russia")],
        [InlineKeyboardButton(text="🇺🇸 America", callback_data="select_server_america")],
        [InlineKeyboardButton(text="🇩🇪 Germany", callback_data="select_server_germany")],
        [
            InlineKeyboardButton(
                text="🇸🇬 Singapore", callback_data="select_server_singapore"
            )
        ],
        [InlineKeyboardButton(text="Orqaga ↩️", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=server_buttons)


# Define a function to create the Accauntim inline keyboard
def create_accauntim_keyboard():
    """Creates an Inline Keyboard Markup for the Accauntim menu."""
    accauntim_buttons = [
        [InlineKeyboardButton(text="Promo kod kiritish", callback_data="enter_promo_code")],
        [InlineKeyboardButton(text="Orqaga ↩️", callback_data="back_to_main")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=accauntim_buttons)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Handles the /start command and displays the main menu.
    """
    logging.info(f"Received /start command from user {message.from_user.id}")
    await message.answer(
        "Assalomu alaykum! Botimizga xush kelibsiz!",
        reply_markup=create_main_menu_keyboard(),
    )
    logging.info(f"Sent welcome message and main menu to user {message.from_user.id}")


# Handler for "💎 Tariflar" button press (from Reply Keyboard)
@dp.message(lambda message: message.text == "💎 Tariflar")
async def handle_tariflar(message: Message):
    logging.info(f"Received '💎 Tariflar' from user {message.from_user.id}")
    await message.answer(
        "Iltimos, server joylashuvini tanlang:",
        reply_markup=create_server_location_keyboard(),
    )
    logging.info(f"Sent server selection menu to user {message.from_user.id}")


# Define handlers for server location selections (using callback queries)
@dp.callback_query(lambda c: c.data and c.data.startswith("select_server_"))
async def process_server_selection(callback_query: CallbackQuery):
    logging.info(
        f"Received server selection callback query '{callback_query.data}' from user {callback_query.from_user.id}"
    )
    server_location = callback_query.data.split("_")[-1]  # e.g., 'russia'
    user_id = str(callback_query.from_user.id)

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
        logging.warning(
            f"User {user_id} selected unknown server location: {server_location}"
        )
        await callback_query.answer("Server topilmadi.", show_alert=True)
        return

    # Determine link type (can be dynamic based on server, for now let's assume vmess for ws, vless for tcp with flow)
    link_type = "vmess" if selected_server.get("network") == "ws" else "vless"
    logging.info(f"User {user_id} selected {server_location}. Generating {link_type} link.")

    try:
        # Generate the VPN link
        generated_link = generate_vpn_link(
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
        if user_id not in users_data:
            users_data[user_id] = {"keys": []}
            logging.info(f"Created new entry for user {user_id} in users_data.")
        users_data[user_id]["keys"].append(generated_link)
        save_users_data(users_data)
        logging.info(f"Saved new key for user {user_id}.")

        # Send the link to the user
        await callback_query.message.answer(
            f"Sizning VPN havolangiz:\n`{generated_link}`", parse_mode="MarkdownV2"
        )
        logging.info(f"Sent VPN link to user {user_id}")

        # Answer the callback query to remove the loading state
        await callback_query.answer("Havola yaratildi!")
        logging.info(f"Answered callback query for user {user_id}")

        # Display the main menu again
        await callback_query.message.answer(
            "Asosiy menyu", reply_markup=create_main_menu_keyboard()
        )
        logging.info(f"Sent main menu to user {user_id}")


    except ValueError as e:
        logging.error(f"ValueError during link generation for user {user_id}: {e}")
        await callback_query.answer(f"Xato: {e}", show_alert=True)
    except Exception as e:
        logging.error(
            f"Error generating or saving link for user {user_id}: {e}", exc_info=True
        )  # Log traceback
        await callback_query.answer("Havolani yaratishda kutilmagan xato yuz berdi.", show_alert=True)


# Handler for "Orqaga ↩️" button in the server selection menu (from Inline Keyboard)
@dp.callback_query(lambda c: c.data == "back_to_main")
async def process_back_to_main(callback_query: CallbackQuery):
    logging.info(
        f"Received 'Orqaga ↩️' callback query from user {callback_query.from_user.id}"
    )
    await callback_query.answer()  # Answer the callback query
    await callback_query.message.answer(
        "Asosiy menyu", reply_markup=create_main_menu_keyboard()
    )
    logging.info(f"Sent main menu to user {callback_query.from_user.id}")


@dp.message(lambda message: message.text == "🔑 Kalitlarim")
async def handle_kalitlarim(message: Message):
    """
    Handles the "🔑 Kalitlarim" button press and displays the user's generated keys.
    """
    logging.info(f"Received '🔑 Kalitlarim' from user {message.from_user.id}")
    user_id = str(message.from_user.id)

    if user_id in users_data and users_data[user_id].get("keys"):
        user_keys = users_data[user_id]["keys"]
        if user_keys:
            logging.info(f"Displaying {len(user_keys)} keys for user {user_id}.")
            # Format the keys into a readable message
            keys_message = "Sizning saqlangan kalitlaringiz:\n\n"
            for i, key in enumerate(user_keys):
                # Escape the dot in the number and any special characters in the key
                escaped_key = key.replace('.', '\\.').replace('-', '\\-').replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]').replace('(', '\\(').replace(')', '\\)').replace('~', '\\~').replace('`', '\\`').replace('>', '\\>').replace('#', '\\#').replace('+', '\\+').replace('-', '\\-').replace('=', '\\=').replace('|', '\\|').replace('{', '\\{').replace('}', '\\}').replace('.', '\\.');
                keys_message += f"{i + 1}\\. `{escaped_key}`\n\n"

            await message.answer(keys_message, parse_mode="MarkdownV2")
        else:
            logging.info(f"User {user_id} has no saved keys.")
            await message.answer("Sizda hali saqlangan kalitlar yo'q.")
    else:
        logging.info(f"User {user_id} has no saved keys in database.")
        await message.answer("Sizda hali saqlangan kalitlar yo'q.")

    # Display the main menu again
    await message.answer("Asosiy menyu", reply_markup=create_main_menu_keyboard())
    logging.info(f"Sent main menu to user {user_id}")


# Handler for "👤 Accauntim" button press (from Reply Keyboard)
@dp.message(lambda message: message.text == "👤 Accauntim")
async def handle_accauntim(message: Message):
    """
    Handles the "👤 Accauntim" button press and displays user account info
    with an inline keyboard for promo code entry.
    """
    logging.info(f"Received '👤 Accauntim' from user {message.from_user.id}")
    user_id = str(message.from_user.id)
    account_info = f"Sizning Accauntingiz:\n\nUser ID: `{user_id}`"  # Display user ID

    await message.answer(
        account_info, reply_markup=create_accauntim_keyboard(), parse_mode="MarkdownV2"
    )
    logging.info(f"Sent account info and inline keyboard to user {user_id}")


# Callback query handler for "Promo kod kiritish" button
@dp.callback_query(lambda c: c.data == "enter_promo_code")
async def process_enter_promo_code(callback_query: CallbackQuery):
    """
    Handles the "Promo kod kiritish" callback query and prompts the user for a promo code.
    """
    logging.info(
        f"Received 'enter_promo_code' callback query from user {callback_query.from_user.id}"
    )
    await callback_query.answer()  # Answer the callback query
    # For now, just prompt the user. Promo code logic will be implemented later.
    await callback_query.message.answer("Iltimos, promo kodingizni kiriting:")
    logging.info(f"Prompted user {callback_query.from_user.id} for promo code.")


# Handler for "📘 Ko'rsatmalar"
@dp.message(lambda message: message.text == "📘 Ko'rsatmalar")
async def handle_korsatmalar(message: Message):
    """
    Handles the "📘 Ko'rsatmalar" button press and displays installation instructions.
    """
    logging.info(f"Received '📘 Ko'rsatmalar' from user {message.from_user.id}")
    instructions_text = """
<b>📘 Ko'rsatmalar</b>

<b>Android uchun:</b>
1. Google Play Store'dan V2RayNG ilovasini yuklab oling.
2. Yuqoridagi VPN havolangizni nusxa oling.
3. Ilovani oching va yuqori o'ng burchakdagi "+" tugmasini bosing.
4. "Import config from Clipboard" ni tanlang.
5. Ulanishni boshlash uchun pastki o'ng burchakdagi dumaloq tugmani bosing.

<b>Windows uchun:</b>
1. V2RayN yoki Qv2ray ilovalaridan birini yuklab oling.
2. Ilovani o'rnating va ishga tushiring.
3. VPN havolangizni nusxa oling.
4. Ilovada 'Import' yoki 'Add' tugmasini toping va havolani joylang.
5. Ulanishni faollashtiring.

<b>iPhone uchun:</b>
1. App Store'dan Shadowrocket, V2RayNG (agar mavjud bo'lsa) yoki boshqa V2Ray/Xray mijozini yuklab oling.
2. Ilovani oching.
3. VPN havolangizni nusxa oling.
4. Ilovada 'Add Server' yoki shunga o'xshash tugmani topib, havolani import qiling.
5. Ulanishni boshlang.

<b>Mac uchun:</b>
1. V2RayX, Qv2ray yoki boshqa mos keladigan mijoz ilovasini yuklab oling.
2. Ilovani o'rnating va oching.
3. VPN havolangizni nusxa oling.
4. Ilovada 'Import' yoki 'Add' tugmasini toping va havolani joylang.
5. Ulanishni faollashtiring.
"""
    await message.answer(instructions_text, parse_mode="HTML")
    logging.info(f"Sent instructions to user {message.from_user.id}")

    # Display the main menu again
    await message.answer("Asosiy menyu", reply_markup=create_main_menu_keyboard())
    logging.info(f"Sent main menu to user {message.from_user.id}")


# Handler for "🆘 Yordam"
@dp.message(lambda message: message.text == "🆘 Yordam")
async def handle_yordam(message: Message):
    """
    Handles the "🆘 Yordam" button press and displays help information.
    """
    logging.info(f"Received '🆘 Yordam' from user {message.from_user.id}")
    help_text = """
<b>🆘 Yordam</b>

<b>Umumiy muammolar va yechimlari:</b>

<b>1. VPN ishlamayapti:</b>
- Internet aloqangizni tekshiring.
- VPN havolasini to'g'ri nusxa olganingizga ishonch hosil qiling.
- Ilovangizda serverni qayta tanlab ko'ring.
- Agar muammo davom etsa, yangi kalit yaratib ko'ring ("💎 Tariflar").

<b>2. Internet sekin:</b>
- Boshqa server joylashuvini tanlab ko'ring ("💎 Tariflar"). Ba'zi serverlar sizning joylashuvingizga yaqinroq bo'lishi mumkin.
- Internet provayderingiz bilan bog'lanib, umumiy internet tezligini tekshiring.

<b>3. Bot ishlamayapti:</b>
- Bir necha daqiqadan keyin qayta urinib ko'ring. Botda texnik ishlar olib borilayotgan bo'lishi mumkin.
- Agar muammo davom etsa, adminstrator bilan bog'lanish uchun "👥 Do‘stim" menyusidagi aloqa ma'lumotlaridan foydalaning (agar mavjud bo'lsa).
"""
    await message.answer(help_text, parse_mode="HTML")
    logging.info(f"Sent help information to user {message.from_user.id}")

    # Display the main menu again
    await message.answer("Asosiy menyu", reply_markup=create_main_menu_keyboard())
    logging.info(f"Sent main menu to user {message.from_user.id}")


@dp.message(lambda message: message.text == "👥 Do'stim")
async def handle_dustim(message: Message):
    """
    Handles the "👥 Do'stim" button press, shows a referral link,
    and a placeholder message about referral tracking.
    """
    logging.info(f"Received '👥 Do'stim' from user {message.from_user.id}")
    user_id = str(message.from_user.id)
    bot_username = "your_bot_username"
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    # Escape special characters for MarkdownV2
    escaped_link = referral_link.replace(".", "\.")
    referral_message = f"""
Sizning referral havolangiz:
`{escaped_link}`

Do'stlaringizni taklif qiling va bonuslarga ega bo'ling\\! \\(Referral hisobi hozircha oddiy\\)
"""
    await message.answer(referral_message, parse_mode="MarkdownV2")
    logging.info(f"Sent referral link to user {user_id}")

    # Display the main menu again
    await message.answer("Asosiy menyu", reply_markup=create_main_menu_keyboard())
    logging.info(f"Sent main menu to user {user_id}")


# Global error handler
@dp.error()
async def errors_handler(update, exception):
    """
    Global error handler to log unhandled exceptions and notify the user.
    """
    logging.error(f"Unhandled exception in update: {update}", exc_info=exception)

    # Attempt to send an error message to the user
    try:
        if update.message:
            await update.message.answer(
                "Kechirasiz, kutilmagan xato yuz berdi. Iltimos, keyinroq urinib ko'ring."
            )
        elif update.callback_query:
            await update.callback_query.message.answer(
                "Kechirasiz, kutilmagan xato yuz berdi. Iltimos, keyinroq urinib ko'ring."
            )
            await update.callback_query.answer()  # Answer the callback query to prevent infinite loading
    except Exception as e:
        logging.error(f"Failed to send error message to user: {e}")


async def main():
    # Add logging for bot startup
    logging.info("Bot is starting...")
    # Make sure user data is loaded before starting polling
    global users_data
    users_data = load_users_data()
    await dp.start_polling(bot, skip_updates=True)
    logging.info("Bot is ready and polling for updates.")

    # Add shutdown handler
    try:
        await asyncio.Event().wait()
    finally:
        logging.info("Bot is shutting down.")
        await bot.session.close()


if __name__ == "__main__":
    # Configure logging level if not already set
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped manually.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)