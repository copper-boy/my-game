from app.orm.game import GameModel
from app.orm.session import ChatModel, PlayerModel, SessionModel


async def create_session(game: GameModel) -> SessionModel:
    session = await SessionModel.create(game=game)
    return session


async def remove_session(session_id: int) -> None:
    session = await SessionModel.get(id=session_id)
    await session.delete()


async def get_session_by_id(id: int) -> SessionModel:
    session = await SessionModel.get(id=id)
    return session


async def get_session_by_chat(chat: ChatModel) -> SessionModel:
    session = await SessionModel.get(chat=chat)
    return session


async def create_chat(chat_id: int,
                      session: SessionModel) -> ChatModel:
    chat = await ChatModel.create(chat_id=chat_id,
                                  session=session)
    return chat


async def get_chat_by_telegram_chat_id(id: int) -> ChatModel:
    chat = await ChatModel.get(chat_id=id)
    return chat


async def create_player(player_id: int,
                        session: SessionModel,
                        pot: int = 0) -> PlayerModel:
    player = await PlayerModel.create(player_id=player_id,
                                      pot=pot,
                                      session=session)
    return player


async def remove_player(player_id: int,
                        chat_id: int) -> None:
    session = await get_session_by_chat(chat_id)

    player = await session.players.filter(player_id=player_id).first()

    await player.delete()


async def get_player_by_session(player_id: int,
                                session: SessionModel) -> PlayerModel:
    player = await PlayerModel.get(player_id=player_id,
                                   session=session)
    return player


async def update_player_pot(player: PlayerModel,
                            pot: int) -> None:
    await player.update_from_dict({
        'pot': player.pot + pot
    })
    await player.save()
