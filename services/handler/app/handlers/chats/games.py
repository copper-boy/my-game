from app.keyboard import get_games_keyboard


async def games_command_handler(bot, message) -> None:
    reply_markup = await get_games_keyboard(app=bot.app)
    await bot.send_message(message='Available games', chat_id=message.chat.id, reply_markup=reply_markup)
