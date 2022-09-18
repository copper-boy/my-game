from aiohttp.client import ClientSession

from app.integration.api import get_theme
from app.schemas.message import CallbackSchema
from app.settings.config import get_api_site_settings


async def theme_callback_handler(bot, callback: CallbackSchema) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(chat_id=callback.message.chat.id)
    if session is None:
        return await bot.send_message(message='Please, select the game!', chat_id=callback.message.chat.id)

    (_, theme_id) = callback.data.split('-')

    async with ClientSession(base_url=get_api_site_settings().API_SITE_BASE_URL) as client:
        theme = await get_theme(client=client, theme_id=int(theme_id))

    if theme is None:
        return await bot.send_message(message=f'@{callback.message_from.username} theme not found on server',
                                      chat_id=callback.message.chat.id)

    await bot.send_message(message=f'@{callback.message_from.username} theme is: {theme["title"]}',
                           chat_id=callback.message.chat.id)
