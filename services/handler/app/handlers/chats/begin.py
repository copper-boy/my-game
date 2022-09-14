from random import choice

from aiohttp import ClientSession

from app.authed_client import set_auth_session

THEMES_MESSAGE = """
Themes:

{}
"""

SELECT_THEME = """
Current player is @{}, please, select theme!
"""


async def get_session(session: ClientSession, bot, chat_id: int) -> dict | None:
    async with session.get(url='http://logic_service:14961/api/v1/logic/get/session',
                           params={
                               'chat_id': chat_id
                           }) as get_session_response:
        if get_session_response.status != 200:
            return await bot.send_message(message='Please, select theme for game!', chat_id=chat_id)
        get_session_json = await get_session_response.json()

        if get_session_json['is_started']:
            return await bot.send_message(message='Game already started!', chat_id=chat_id)

    return get_session_json


async def get_questions(session: ClientSession, theme_id: int) -> list[str]:
    async with session.get('http://logic_service:14961/api/v1/logic/get/questions',
                           params={
                               'theme_id': theme_id
                           }) as get_questions_response:
        get_questions_json = await get_questions_response.json()

    result = [str(question['cost']) for question in get_questions_json]
    return result


async def send_themes(session: ClientSession, bot, game_id: int, chat_id: int) -> None:
    async with session.get(url='http://logic_service:14961/api/v1/logic/get/themes',
                           params={
                               'game_id': game_id
                           }) as get_themes_response:
        get_themes_json = await get_themes_response.json()

        themes: list[str] = []
        for theme in get_themes_json:
            questions = await get_questions(session=session, theme_id=theme['id'])
            themes.append(f'{theme["title"]} {" ".join(questions)}')

        formatted_text = THEMES_MESSAGE.format('\n'.join(themes))
        await bot.send_message(message=formatted_text, chat_id=chat_id)


async def get_random_player(session: ClientSession, chat_id: int) -> dict:
    async with session.get('http://logic_service:14961/api/v1/logic/get/players',
                           params={
                               'chat_id': chat_id
                           }) as get_players_response:
        get_players_json = await get_players_response.json()
    player = choice(get_players_json)
    return player


async def set_current_player(session: ClientSession, chat_id: int, player_id: int) -> dict:
    async with session.put('http://logic_service:14961/api/v1/logic/update/session/current_player',
                           params={
                               'chat_id': chat_id,
                               'player_id': player_id
                           }) as response:
        json = await response.json()
    return json


async def start_game(session: ClientSession, chat_id: int) -> dict:
    async with session.put('http://logic_service:14961/api/v1/logic/update/session/start',
                           params={
                               'chat_id': chat_id
                           }) as response:
        json = await response.json()
    return json


async def begin_command_handler(bot, message):
    async with ClientSession() as session:
        await set_auth_session(session)

        chat_session = await get_session(session=session, bot=bot, chat_id=message.chat.id)

        if chat_session is None:
            return None

        await send_themes(session=session, bot=bot, game_id=chat_session['game_id'], chat_id=message.chat.id)

        player = await get_random_player(session=session, chat_id=message.chat.id)

        await set_current_player(session=session, chat_id=message.chat.id, player_id=player['player_id'])
        await start_game(session=session, chat_id=message.chat.id)

    username = await bot.get_chat_member_username(chat_id=message.chat.id, user_id=player['player_id'])
    formatted_text = SELECT_THEME.format(username)
    await bot.send_message(message=formatted_text, chat_id=message.chat.id)
