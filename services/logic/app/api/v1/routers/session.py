from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query
from fastapi.responses import JSONResponse

from app.orm.session import player_pydantic_out, session_pydantic_out
from app.utils.game import get_game_by_id
from app.utils.session import (create_player, create_session,
                               get_player_by_session, get_session_by_chat_id,
                               get_session_by_id, remove_player,
                               remove_session, update_player, update_session)

router = APIRouter()


@router.post('/create/session')
async def post_session(game_id: int = Query(...), chat_id: int = Query(...)) -> session_pydantic_out:
    game = await get_game_by_id(game_id)
    if game is None:
        raise HTTPException(status_code=404,
                            detail=f'game with {game_id=} not found')

    session = await create_session(game.id, chat_id)
    session_pydantic = await session_pydantic_out.from_tortoise_orm(session)

    return session_pydantic


@router.post('/create/player')
async def post_player(chat_id: int = Query(...), player_id: int = Query(...)) -> player_pydantic_out:
    session = await get_session_by_chat_id(chat_id=chat_id)

    if await get_player_by_session(player_id=player_id, session=session):
        raise HTTPException(status_code=409,
                            detail='player already exists')

    player = await create_player(player_id=player_id, session=session)
    player_pydantic = await player_pydantic_out.from_tortoise_orm(player)

    return player_pydantic


@router.put('/update/session/game_id')
async def put_session_game_id(game_id: int = Query(...), chat_id: int = Query(...)) -> session_pydantic_out:
    if await get_game_by_id(game_id) is None:
        raise HTTPException(status_code=404,
                            detail='game not found')

    session = await get_session_by_chat_id(chat_id)
    if session is None:
        raise HTTPException(status_code=404,
                            detail='session not found')

    await update_session(session=session, params={
        'game_id': game_id
    })

    session_pydantic = await session_pydantic_out.from_tortoise_orm(session)

    return session_pydantic


@router.put('/update/session/current_player')
async def put_session_current_player(player_id: int = Query(...), chat_id: int = Query(...)) -> session_pydantic_out:
    session = await get_session_by_chat_id(chat_id=chat_id)
    if session is None:
        raise HTTPException(status_code=404,
                            detail='session not found')

    player = await get_player_by_session(session=session, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=403,
                            detail='player not in game')
    await update_session(session=session, params={
        'current_player': player_id
    })

    session_pydantic = await session_pydantic_out.from_tortoise_orm(session)

    return session_pydantic


@router.put('/update/session/start')
async def put_session_start(chat_id: int = Query(...)) -> session_pydantic_out:
    session = await get_session_by_chat_id(chat_id=chat_id)
    if session is None:
        raise HTTPException(status_code=404,
                            detail='session not found')

    await update_session(session=session, params={
        'is_started': True
    })

    session_pydantic = await session_pydantic_out.from_tortoise_orm(session)

    return session_pydantic


@router.delete('/delete/session')
async def delete_session(session_id: int = Query(...)) -> JSONResponse:
    try:
        await remove_session(session_id)
    except AttributeError:
        raise HTTPException(status_code=404,
                            detail=f'session with {session_id=} doesnt exists')
    else:
        return JSONResponse(status_code=200,
                            content={
                                'detail': 'deleted'
                            })


@router.delete('/delete/player')
async def delete_player(player_id: int = Query(...), chat_id: int = Query(...)) -> JSONResponse:
    try:
        await remove_player(player_id, chat_id)
    except AttributeError:
        raise HTTPException(status_code=404,
                            detail=f'player with {player_id=} doesnt exists')
    else:
        return JSONResponse(status_code=200,
                            content={
                                'detail': 'deleted'
                            })


@router.get('/get/session')
async def get_session(chat_id: int = Query(...)) -> session_pydantic_out:
    session = await get_session_by_chat_id(chat_id=chat_id)
    session_pydantic = await session_pydantic_out.from_tortoise_orm(session)

    return session_pydantic


@router.get('/get/players')
async def get_players(chat_id: int = Query(...)) -> list[player_pydantic_out]:
    session = await get_session_by_chat_id(chat_id=chat_id)
    players_pydantic = [await player_pydantic_out.from_tortoise_orm(player) async for player in session.players]

    return players_pydantic


@router.get('/get/player')
async def get_player(chat_id: int = Query(...), player_id: int = Query(...)) -> player_pydantic_out:
    session = await get_session_by_chat_id(chat_id=chat_id)
    player = await get_player_by_session(player_id=player_id, session=session)
    player_pydantic = await player_pydantic_out.from_tortoise_orm(player)

    return player_pydantic


@router.put('/update/player/pot')
async def put_player_pot(chat_id: int = Query(...),
                         player_id: int = Query(...),
                         pot: int = Query(...)) -> player_pydantic_out:
    session = await get_session_by_chat_id(chat_id=chat_id)
    player = await get_player_by_session(player_id=player_id, session=session)

    await update_player(player=player, params={
        'pot': player.pot + pot
    })

    player_pydantic = await player_pydantic_out.from_tortoise_orm(player)

    return player_pydantic
