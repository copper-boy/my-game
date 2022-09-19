from app.integration.api import get_games


async def games_command_handler(bot, message) -> None:
    games_json = await get_games(client=bot.app.store.aiohttp_session_accessor.aiohttp_session)

    reply_markup = {
        'inline_keyboard': [
        ]
    }

    for game in games_json:
        reply_markup['inline_keyboard'].append([
            {
                'text': game['name'],
                'callback_data': f'game-{game["id"]}'
            }
        ])

    await bot.send_message(message='Available games', chat_id=message.chat.id, reply_markup=reply_markup)
