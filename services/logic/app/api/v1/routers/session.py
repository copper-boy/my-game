from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query
from fastapi.responses import JSONResponse

from orm.session import (chat_pydantic_out, player_pydantic_out,
                         session_pydantic_out)
from utils.game import get_game_by_id
from utils.session import (create_chat, create_player, create_session,
                           get_chat_by_telegram_chat_id, get_player_by_session,
                           get_session_by_chat, get_session_by_id,
                           remove_player, remove_session, update_player_pot)

router = APIRouter()


@router.post('/create/session')
async def post_session(game_id: int = Query(...)) -> session_pydantic_out:
    game = await get_game_by_id(game_id)
    session = await create_session(game)

    return session


@router.post('/create/chat')
async def post_chat(chat_id: int = Query(...),
                    session_id: int = Query(...)) -> chat_pydantic_out:
    session = await get_session_by_id(session_id)

    if await get_chat_by_telegram_chat_id(id=chat_id):
        raise HTTPException(status_code=409,
                            detail='chat already exits')

    chat = await create_chat(chat_id=chat_id,
                             session=session)

    return chat


@router.post('/create/player')
async def post_player(chat_id: int = Query(...),
                      player_id: int = Query(...)) -> player_pydantic_out:
    chat = await get_chat_by_telegram_chat_id(id=chat_id)
    session = await get_session_by_chat(chat=chat.id)

    if await get_player_by_session(player_id=player_id,
                                   session=session):
        raise HTTPException(status_code=409,
                            detail='player already exists')

    player = await create_player(player_id=player_id,
                                 session=session)

    return player


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
async def delete_player(player_id: int = Query(...),
                        chat_id: int = Query(...)) -> JSONResponse:
    try:
        await remove_player(player_id,
                            chat_id)
    except AttributeError:
        raise HTTPException(status_code=404,
                            detail=f'player with {player_id=} doesnt exists')
    else:
        return JSONResponse(status_code=200,
                            content={
                                'detail': 'deleted'
                            })


@router.get('/get/chat')
async def get_chat(chat_id: int = Query(...)) -> chat_pydantic_out:
    chat = await get_chat_by_telegram_chat_id(chat_id)

    return chat


@router.get('/get/session')
async def get_session(chat_id: int = Query(...)) -> session_pydantic_out:
    chat = await get_chat_by_telegram_chat_id(id=chat_id)
    session = await get_session_by_chat(chat=chat.id)

    return session


@router.get('/get/players')
async def get_players(chat_id: int = Query(...)) -> list[player_pydantic_out]:
    chat = await get_chat_by_telegram_chat_id(id=chat_id)
    session = await get_session_by_chat(chat=chat.id)
    raw_players = [player async for player in session.players]

    return raw_players


@router.get('/get/player')
async def get_player(chat_id: int = Query(...),
                     player_id: int = Query(...)) -> player_pydantic_out:
    chat = await get_chat_by_telegram_chat_id(chat_id=chat_id)
    session = await get_session_by_chat(chat=chat)
    player = await get_player_by_session(player_id=player_id,
                                         session=session)

    return player


@router.put('/update/player/pot')
async def put_player_pot(chat_id: int = Query(...),
                         player_id: int = Query(...),
                         pot: int = Query(...)) -> player_pydantic_out:
    chat = await get_chat_by_telegram_chat_id(id=chat_id)
    session = await get_session_by_chat(chat=chat.id)
    player = await get_player_by_session(player_id=player_id,
                                         session=session)

    await update_player_pot(player=player,
                            pot=pot)

    return player
