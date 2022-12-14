from __future__ import annotations

from aiohttp.client import ClientSession

from app.settings.config import get_admin_settings, get_api_site_settings


async def get_game(client: ClientSession, game_id: int) -> dict | None:
    async with client.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/games/{game_id}',
                          params={
                              'token': get_admin_settings().INFINITY_ADMIN_TOKEN
                          }) as response:
        if response.status == 404:
            return None

        json = await response.json()

    return json


async def get_games(client: ClientSession) -> dict:
    async with client.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/games',
                          params={
                              'token': get_admin_settings().INFINITY_ADMIN_TOKEN,
                          }) as games_response:
        json = await games_response.json()

    return json


async def get_answer(client: ClientSession, question_id: int) -> dict | None:
    async with client.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/answers/{question_id}',
                          params={
                              'token': get_admin_settings().INFINITY_ADMIN_TOKEN
                          }) as response:
        if response.status == 404:
            return None

        json = await response.json()

    return json


async def get_question(client: ClientSession, question_id: int) -> dict | None:
    async with client.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/questions/{question_id}',
                          params={
                              'token': get_admin_settings().INFINITY_ADMIN_TOKEN
                          }) as response:
        if response.status == 404:
            return None

        json = await response.json()

    return json


async def get_questions(session: ClientSession, theme_id: int) -> list[dict]:
    async with session.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/questions',
                           params={
                               'token': get_admin_settings().INFINITY_ADMIN_TOKEN,
                               'theme_id': theme_id
                           }) as get_questions_response:
        get_questions_json = await get_questions_response.json()

    reply_markup: list[dict] = []
    for question in get_questions_json:
        reply_markup.append({
            'text': question['cost'],
            'callback_data': f'question-{question["id"]}'
        })

    return reply_markup


async def get_questions_count(session: ClientSession, theme_id: int) -> int:
    async with session.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/count/questions',
                           params={
                               'token': get_admin_settings().INFINITY_ADMIN_TOKEN,
                               'theme_id': theme_id
                           }) as response:
        response = await response.json()

    return response['count']


async def get_theme(client: ClientSession, theme_id: int) -> dict | None:
    async with client.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/themes/{theme_id}',
                          params={
                              'token': get_admin_settings().INFINITY_ADMIN_TOKEN
                          }) as response:
        if response.status == 404:
            return None
        json = await response.json()

    return json


async def get_themes(session: ClientSession, game_id: int) -> tuple[int, dict]:
    count = 0
    reply_markup = {
        'inline_keyboard': []
    }

    async with session.get(url=f'{get_api_site_settings().API_SITE_BASE_URL}/api/v1/admin/themes',
                           params={
                               'token': get_admin_settings().INFINITY_ADMIN_TOKEN,
                               'game_id': game_id
                           }) as get_themes_response:
        get_themes_json = await get_themes_response.json()

    for theme in get_themes_json:
        count += await get_questions_count(session=session, theme_id=theme['id'])
        questions = await get_questions(session=session, theme_id=theme['id'])
        keyboard = [
            {
                'text': theme['title'],
                'callback_data': f'theme-{theme["id"]}'
            },
        ]
        keyboard.extend(questions)

        reply_markup['inline_keyboard'].append(keyboard)

    return count, reply_markup
