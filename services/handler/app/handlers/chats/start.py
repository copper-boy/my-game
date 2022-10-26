from app.schemas.message import MessageSchema
from app.utils.decorators.handle_exceptions import handle_exceptions
from app.utils.decorators.session import transaction


@handle_exceptions
@transaction
async def start_command_handler(bot, message: MessageSchema, sql_session=None) -> None:
    session = await bot.app.store.sessions.create_session(sql_session=sql_session,
                                                          chat_id=message.chat.id)
    await bot.app.store.game_states.create_game_state(sql_session=sql_session,
                                                      session=session)

    await bot.send_message(message='Now you can use me!',
                           chat_id=message.chat.id)
