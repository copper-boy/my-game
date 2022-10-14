from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.session import SessionModel


async def get_end_message(bot,
                          sql_session: AsyncSession,
                          session: SessionModel,
                          chat_id: str) -> str:
    bot_answer: list[str] = []
    for player in await bot.app.store.players.get_players_by_session_id(sql_session=sql_session,
                                                                        session_id=session.id):
        username = await bot.get_chat_member_username(chat_id=chat_id, user_id=player.telegram_id)
        s = f'@{username} has pot {player.pot}, gg!'
        bot_answer.append(s)

    return '\n'.join(bot_answer)
