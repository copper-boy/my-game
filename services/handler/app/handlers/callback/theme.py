from app.integration.api import get_theme
from app.schemas.message import CallbackSchema
from app.utils.decorators.session import transaction


@transaction
async def theme_callback_handler(bot, callback: CallbackSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session,
                                                                  chat_id=callback.message.chat.id)
    if session is None:
        return await bot.send_message(message=bot.message_helper.bad_message(username=callback.message_from.username),
                                      chat_id=callback.message.chat.id)

    (_, theme_id) = callback.data.split('-')

    theme = await get_theme(client=bot.app.store.aiohttp_session_accessor.aiohttp_session, theme_id=int(theme_id))

    if theme is None:
        return await bot.send_message(message=bot.message_helper.bad_message(username=callback.message_from.username),
                                      chat_id=callback.message.chat.id)

    await bot.send_message(message=f'@{callback.message_from.username} theme is: {theme["title"]}',
                           chat_id=callback.message.chat.id)
