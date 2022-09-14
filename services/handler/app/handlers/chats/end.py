from aiohttp import ClientSession


async def delete_session(session: ClientSession, chat_id: int) -> None:
    async with session.delete():
        pass

async def end_command_handler(bot, message):
    async with ClientSession() as session:
        pass

