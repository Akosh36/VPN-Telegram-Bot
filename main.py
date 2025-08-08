import asyncio
import logging
from aiogram import Bot, Dispatcher

# Import configurations
from app.config import BOT_TOKEN, logger

# Import managers and services
from app.data.user_data_manager import UserDataManager
from app.services.vpn_link_generator import VPNLinkGenerator

# Import handler registration functions
from app.handlers.message_handlers import register_message_handlers
from app.handlers.callback_query_handlers import register_callback_query_handlers
from app.handlers.error_handlers import register_error_handler

logger.info("Starting bot initialization...")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Initialize managers and services
user_data_manager = UserDataManager()
vpn_link_generator = VPNLinkGenerator()

# Register handlers
register_message_handlers(dp, user_data_manager)
register_callback_query_handlers(dp, user_data_manager, vpn_link_generator)
register_error_handler(dp)

logger.info("Bot and Dispatcher initialized, handlers registered.")

async def main():
    logger.info("Bot is starting...")
    # No need to explicitly load users_data here, UserDataManager does it on instantiation
    # Ensure bot is ready and polling for updates
    await dp.start_polling(bot, skip_updates=True)
    logger.info("Bot is ready and polling for updates.")

    # Keep the bot running until interrupted
    try:
        await asyncio.Event().wait()
    finally:
        logger.info("Bot is shutting down.")
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually.")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}", exc_info=True)