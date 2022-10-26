from app.schemas.message import MessageSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction
from app.utils.delete import delete_session
from app.utils.end_message import get_end_message


@handle_exceptions
@transaction
async def end_command_handler(bot, message: MessageSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(sql_session=sql_session, chat_id=message.chat.id)

    if not bot.is_user_admin(chat_id=message.chat.id, user_id=message.message_from.id):
        raise RuntimeError

    bot_answer: list[str] = []
    for player in await bot.app.store.players.get_players_by_session_id(sql_session=sql_session,
                                                                        session_id=session.id):
        username = await bot.get_chat_member_username(chat_id=message.chat.id, user_id=player.telegram_id)
        s = f'@{username} has pot {player.pot}, gg!'
        bot_answer.append(s)

    await bot.send_message(message='\n'.join(bot_answer), chat_id=message.chat.id)

    await delete_session(store=bot.app.store,
                         sql_session=sql_session,
                         session=session)
