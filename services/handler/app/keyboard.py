from app.integration.api import get_games


def get_join_exit_keyboard() -> dict:
    return {
        'inline_keyboard': [
            [
                {
                    'text': 'Join',
                    'callback_data': 'join'
                },
                {
                    'text': 'Exit',
                    'callback_data': 'exit'
                }
            ]
        ]
    }


async def get_games_keyboard(app) -> dict:
    games_json = await get_games(client=app.store.aiohttp_session_accessor.aiohttp_session)

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

    return reply_markup
