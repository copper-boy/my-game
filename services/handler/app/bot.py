from asyncio import Queue, ensure_future, get_event_loop
from logging import getLogger
from re import compile

from aiohttp import ClientSession
from aiohttp.web import Application
from asyncpool import AsyncPool

from app.handlers import bad_message
from app.handlers.actions import answer
from app.handlers.callback import answer as answer_callback
from app.handlers.callback import exit, game, join, question, theme
from app.handlers.chats import begin, games
from app.handlers.helpers import about, help
from app.schemas.message import (CallbackSchema, load_message_from_schema,
                                 load_message_schema)

logger = getLogger('bot')

pattern_command = compile(r'/\w+')
pattern_callback = compile(r'[A-Za-z]+')

handlers = {
    '/about': about.about_command_handler,
    '/help': help.help_command_handler,

    '/games': games.games_command_handler,

    '/begin': begin.begin_command_handler,

    '/answer': answer.answer_command_handler,
}

handlers_callback = {
    'game': game.game_callback_handler,

    'join': join.join_callback_handler,
    'exit': exit.exit_callback_handler,

    'theme': theme.theme_callback_handler,
    'question': question.question_callback_handler,

    'answer': answer_callback.answer_callback_handler,
}


class Bot:
    app: Application
    bot_token: str

    def __init__(self, application: Application, bot_token: str) -> None:
        self.app = application
        self.bot_token = bot_token

    @staticmethod
    async def result_reader(queue: Queue) -> None:
        while True:
            value = await queue.get()
            if value is True:
                break

    async def handle_update(self, update: dict, queue: Queue) -> None:
        if update.get('message', None) is not None:
            message = update.get('message')
            message_schema = load_message_schema(message=message)

            for command in pattern_command.findall(message_schema.text):
                handler = handlers.get(command, bad_message.bad_message_command_handler)
                result = await handler(bot=self, message=message_schema)
                await queue.put(result)
        if update.get('callback_query', None) is not None:
            callback_query = update.get('callback_query')

            message_from_schema = load_message_from_schema(message_from=callback_query['from'])
            message_schema = load_message_schema(message=callback_query['message'])

            callback = CallbackSchema(callback_id=callback_query['id'],
                                      message_from=message_from_schema,
                                      message=message_schema,
                                      data=callback_query['data'])

            for command in pattern_callback.findall(callback.data):
                handler = handlers_callback.get(command, bad_message.bad_message_callback_handler)
                result = await handler(bot=self, callback=callback)
                await queue.put(result)

    async def handle(self, updates: list) -> None:
        queue = Queue()
        loop = get_event_loop()
        future = ensure_future(coro_or_future=self.result_reader(queue=queue), loop=loop)

        async with AsyncPool(loop=loop, num_workers=5, name='UpdatePool',
                             logger=logger, worker_co=self.handle_update) as pool:
            for update in updates:
                await pool.push(update, queue)

        await queue.put(True)
        await future

    async def get_chat_member_username(self, chat_id: int, user_id: int) -> str:
        async with ClientSession(base_url='https://api.telegram.org') as session:
            async with session.get(url=f'/bot{self.bot_token}/getChatMember',
                                   params={
                                       'chat_id': chat_id,
                                       'user_id': user_id
                                   }) as response:
                json = await response.json()
        return json['result']['user']['username']

    async def send_message(self, chat_id: int, message: str, reply_markup: dict | None = None) -> None:
        data = {
            'chat_id': chat_id,
            'text': message
        }
        if reply_markup:
            data['reply_markup'] = reply_markup

        async with ClientSession(base_url='https://api.telegram.org') as session:
            async with session.post(url=f'/bot{self.bot_token}/sendMessage',
                                    json=data) as response:
                json = await response.json()
        logger.info(json)

    async def send_sticker(self, chat_id: int, sticker: str) -> None:
        async with ClientSession(base_url='https://api.telegram.org') as session:
            async with session.post(url=f'/bot{self.bot_token}/sendSticker',
                                    json={
                                        'chat_id': chat_id,
                                        'sticker': sticker
                                    }) as response:
                json = await response.json()
        logger.info(json)
