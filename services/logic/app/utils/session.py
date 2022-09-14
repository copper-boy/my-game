from app.orm.session import PlayerModel, SessionModel


async def create_session(game_id: int, chat_id: int) -> SessionModel:
    session = await SessionModel.create(game_id=game_id, chat_id=chat_id)
    return session


async def remove_session(session_id: int) -> None:
    session = await SessionModel.get(id=session_id)
    await session.delete()


async def get_session_by_id(id: int) -> SessionModel:
    session = await SessionModel.get(id=id)
    return session


async def get_session_by_chat_id(chat_id: int) -> SessionModel:
    session = await SessionModel.get(chat_id=chat_id)
    return session


async def create_player(player_id: int,
                        session: SessionModel,
                        pot: int = 0) -> PlayerModel:
    player = await PlayerModel.create(player_id=player_id,
                                      pot=pot,
                                      session=session)
    return player


async def remove_player(player_id: int,
                        chat_id: int) -> None:
    session = await get_session_by_chat_id(chat_id)

    player = await session.players.filter(player_id=player_id).first()

    await player.delete()


async def get_player_by_session(player_id: int,
                                session: SessionModel) -> PlayerModel:
    player = await PlayerModel.get_or_none(player_id=player_id,
                                           session=session)
    return player


async def update_player(player: PlayerModel, params: dict) -> None:
    await player.update_from_dict(params)
    await player.save()


async def update_session(session: SessionModel, params: dict) -> None:
    await session.update_from_dict(params)
    await session.save()
