from aiohttp.client import ClientSession

from app.integration.api import get_games
from app.settings.config import get_api_site_settings


async def games_command_handler(bot, message) -> None:
    async with ClientSession(base_url=get_api_site_settings().API_SITE_BASE_URL) as client:
        games_json = await get_games(client=client)

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
