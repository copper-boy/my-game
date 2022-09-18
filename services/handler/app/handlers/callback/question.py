from aiohttp.client import ClientSession

from app.integration.api import get_question
from app.orm.game_state import GameStateEnum
from app.schemas.message import CallbackSchema
from app.settings.config import get_api_site_settings


async def question_callback_handler(bot, callback: CallbackSchema) -> None:
    session = await bot.app.store.sessions.get_session_by_chat_id(chat_id=callback.message.chat.id)

    if session:
        game_state = await bot.app.store.game_states.get_game_state_by_session_id(session_id=session.id)
        if game_state.state != GameStateEnum.WAIT_FOR_PLAYER_ACTION:
            return await bot.send_message(message='Unable to select a question!', chat_id=callback.message.chat.id)
    else:
        return await bot.send_message(message='The game must be started!', chat_id=callback.message.chat.id)

    player = await bot.app.store.players.get_player_by_telegram_id(session_id=session.id,
                                                                   telegram_id=callback.message_from.id)
    if player is None:
        return await bot.send_message(message=f'@{callback.message_from.username} you should be in the game!',
                                      chat_id=callback.message.chat.id)
    if game_state.current_player != player.id:
        return await bot.send_message(message=f'@{callback.message_from.username} you are not a current player!',
                                      chat_id=callback.message.chat.id)

    (_, question_id) = callback.data.split('-')

    question_session = await bot.app.store.questions_sessions.get_question_session_by_id(session_id=session.id,
                                                                                         question_id=question_id)

    if question_session:
        return await bot.send_message(
            message=f'@{callback.message_from.username} the question has already been selected in the game',
            chat_id=callback.message.chat.id)

    async with ClientSession(base_url=get_api_site_settings().API_SITE_BASE_URL) as client:
        question = await get_question(client=client, question_id=int(question_id))

    if question is None:
        return await bot.send_message(message='The question does not exist on the server',
                                      chat_id=callback.message.chat.id)
    title = question['title']

    await bot.send_message(message=f'The question is: {title}', chat_id=callback.message.chat.id, reply_markup={
        'inline_keyboard': [
            [
                {
                    'text': 'Answer',
                    'callback_data': f'answer-{question_id}'
                }
            ]
        ]
    })
    await bot.app.store.questions_sessions.create_question_session(session=session,
                                                                   question_id=int(question_id))
    await bot.app.store.game_states.update_game_state(game_state_id=game_state.id,
                                                      current_question_id=int(question_id),
                                                      current_player=0,
                                                      state=GameStateEnum.WAIT_FOR_PLAYER_ANSWER)
