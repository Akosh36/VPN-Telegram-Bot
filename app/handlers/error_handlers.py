import logging
from aiogram import Router
from aiogram.types import Update

logger = logging.getLogger(__name__)

def register_error_handler(router: Router):
    @router.error()
    async def errors_handler(update: Update, exception: Exception):
        """
        Global error handler to log unhandled exceptions and notify the user.
        """
        logger.error(f"Unhandled exception in update: {update}", exc_info=exception)

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
            logger.error(f"Failed to send error message to user: {e}")
