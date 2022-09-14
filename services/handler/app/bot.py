from re import compile
from logging import getLogger

from aiohttp import ClientSession

from app.schemas.message import MessageSuperGroupSchema, ChatSuperGroupSchema, MessageFromSchema
from app.handlers import bad_message
from app.handlers.helpers import help, about
from app.handlers.chats import begin, end, games, select_game, current_game
from app.handlers.players import join, exit
from app.handlers.actions import answer, select_theme

logger = getLogger('bot')

pattern = compile(r'/\w+')

handlers = {
    '/about': about.about_command_handler,
    '/help': help.help_command_handler,
    '/begin': begin.begin_command_handler,
    '/end': end.end_command_handler,
    '/games': games.games_command_handler,
    '/select_game': select_game.select_game_command_handler,
    '/current_game': current_game.current_game_command_handler,
    '/join': join.join_command_handler,
    '/exit': exit.exit_command_handler,
   # '/answer': answer.answer_command_handler,
   # '/select_theme': select_theme.select_theme_command_handler,
}


class Bot:
    bot_token: str

    def __init__(self, bot_token: str) -> None:
        self.bot_token = bot_token

    async def handle(self, updates: list) -> None:
        for update in updates:
            message = update['message']

            match message['chat']['type']:
                case 'supergroup' | 'group':
                    message_from_schema = MessageFromSchema(id=message['from']['id'],
                                                            username=message['from']['username'])
                    chat_schema = ChatSuperGroupSchema(id=message['chat']['id'],
                                                       title=message['chat']['title'])
                    message_schema = MessageSuperGroupSchema(message_id=message['message_id'],
                                                             message_from=message_from_schema,
                                                             chat=chat_schema,
                                                             text=message['text'])
                case _:
                    return await bad_message.bad_message_handler(self, message['chat']['id'])
            for command in pattern.findall(message_schema.text):
                handler = handlers.get(command, bad_message.bad_message_handler)
                await handler(bot=self, message=message_schema)

    async def get_chat_member_username(self, chat_id: int, user_id: int) -> str:
        async with ClientSession(base_url='https://api.telegram.org') as session:
            async with session.get(url=f'/bot{self.bot_token}/getChatMember',
                                   params={
                                       'chat_id': chat_id,
                                       'user_id': user_id
                                   }) as response:
                json = await response.json()

        return json['result']['user']['username']

    async def send_message(self, chat_id: int, message: str) -> None:
        async with ClientSession(base_url='https://api.telegram.org') as session:
            async with session.post(url=f'/bot{self.bot_token}/sendMessage',
                                    json={
                                        'chat_id': chat_id,
                                        'text': message
                                    }) as response:
                logger.info(await response.json())

    async def send_sticker(self, chat_id: int, sticker: str) -> None:
        async with ClientSession(base_url='https://api.telegram.org') as session:
            async with session.post(url=f'/bot{self.bot_token}/sendSticker',
                                    json={
                                        'chat_id': chat_id,
                                        'sticker': sticker
                                    }) as response:
                logger.info(await response.json())
