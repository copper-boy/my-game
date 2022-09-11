from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query

from orm.game import (answer_pydantic_in, answer_pydantic_out,
                      game_pydantic_in, game_pydantic_out,
                      question_pydantic_in, question_pydantic_out,
                      theme_pydantic_in, theme_pydantic_out)
from utils.game import (create_answer, create_game, create_question,
                        create_theme, get_answer_by_question, get_game_by_id,
                        get_game_list, get_question_by_id, get_theme_by_id)

router = APIRouter()


@router.post('/create/answer')
async def post_answer(data: answer_pydantic_in, question_id: int = Query(...)) -> answer_pydantic_out:
    question = await get_question_by_id(question_id)

    if await get_answer_by_question(question):
        raise HTTPException(status_code=409,
                            detail='answer already exists')

    answer = await create_answer(**data.__dict__,
                                 question=question)

    return answer


@router.post('/create/game')
async def post_game(data: game_pydantic_in) -> game_pydantic_out:
    game = await create_game(**data.__dict__)

    return game


@router.post('/create/theme')
async def post_theme(data: theme_pydantic_in, game_id: int = Query(...)) -> theme_pydantic_out:
    game = await get_game_by_id(game_id)

    if await game.themes.filter(title=data.title).first():
        raise HTTPException(status_code=409,
                            detail='theme already exists')

    theme = await create_theme(**data.__dict__,
                               game=game)

    return theme


@router.post('/create/question')
async def post_question(data: question_pydantic_in, theme_id: int = Query(...)) -> question_pydantic_out:
    theme = await get_theme_by_id(theme_id)

    if await theme.questions.filter(theme=theme).first():
        raise HTTPException(status_code=409,
                            detail='question already exists')

    question = await create_question(**data.__dict__,
                                     theme=theme)

    return question


@router.get('/get/games')
async def game_list() -> dict:
    games = await get_game_list()
    result: list[game_pydantic_out] = [game_pydantic_out.from_orm(game) async for game in games]

    return {
        'result': result
    }


@router.get('/get/themes')
async def list_theme(game_id: int = Query(...)) -> dict:
    game = await get_game_by_id(game_id)
    result: list[theme_pydantic_out] = [theme_pydantic_out.from_orm(theme) async for theme in game.themes]

    return {
        'result': result
    }


@router.get('/get/questions')
async def list_questions(theme_id: int = Query(...)):
    theme = await get_theme_by_id(theme_id)
    result: list[question_pydantic_out] = [question_pydantic_out.from_orm(question) async for question in
                                           theme.questions]

    return {
        'result': result
    }


@router.get('/get/question')
async def get_question(theme_id: int = Query(...),
                       cost: int = Query(...)) -> question_pydantic_out:
    theme = await get_theme_by_id(theme_id)
    question = await theme.questions.filter(cost=cost)

    return question


@router.get('/get/answer')
async def get_answer(question_id: int = Query(...)) -> answer_pydantic_out:
    question = await get_question_by_id(question_id)
    answer = await get_answer_by_question(question)

    return answer
