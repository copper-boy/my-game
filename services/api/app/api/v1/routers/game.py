from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query, Path, Header

from app.orm.game import (answer_pydantic_in, answer_pydantic_out,
                          game_pydantic_in, game_pydantic_out,
                          question_pydantic_in, question_pydantic_out,
                          theme_pydantic_in, theme_pydantic_out)
from app.utils.game import (create_answer, create_game, create_question,
                            create_theme, get_answer_by_question,
                            get_game_by_id, get_game_list, get_question_by_id,
                            get_theme_by_id)

router = APIRouter()


@router.post('/answer', response_model=answer_pydantic_out)
async def post_answer(data: answer_pydantic_in, question_id: int = Query(...), token: str = Query(...)) -> answer_pydantic_out:
    question = await get_question_by_id(question_id)
    if await get_answer_by_question(question):
        raise HTTPException(status_code=409,
                            detail='answer already exists')

    answer = await create_answer(correct=data.correct, question=question)
    answer_pydantic = await answer_pydantic_out.from_tortoise_orm(answer)

    return answer_pydantic


@router.post('/game', response_model=game_pydantic_out)
async def post_game(data: game_pydantic_in, token: str = Query(...)) -> game_pydantic_out:
    game = await create_game(**data.dict())
    game_pydantic = await game_pydantic_out.from_tortoise_orm(game)

    return game_pydantic


@router.post('/theme', response_model=theme_pydantic_out)
async def post_theme(data: theme_pydantic_in, token: str = Query(...), game_id: int = Query(...)) -> theme_pydantic_out:
    game = await get_game_by_id(game_id)

    if await game.themes.filter(title=data.title).first():
        raise HTTPException(status_code=409,
                            detail='theme already exists')

    theme = await create_theme(**data.dict(), game=game)
    theme_pydantic = await theme_pydantic_out.from_tortoise_orm(theme)

    return theme_pydantic


@router.post('/question', response_model=question_pydantic_out)
async def post_question(data: question_pydantic_in, token: str = Query(...), theme_id: int = Query(...)) -> question_pydantic_out:
    theme = await get_theme_by_id(theme_id)

    question = await create_question(**data.dict(), theme=theme)
    question_pydantic = await question_pydantic_out.from_tortoise_orm(question)

    return question_pydantic


@router.get('/games/{game_id}', response_model=game_pydantic_out)
async def get_game(token: str = Query(...), game_id: int = Path(...)) -> game_pydantic_out:
    game = await get_game_by_id(game_id)
    game_pydantic = await game_pydantic_out.from_tortoise_orm(game)

    return game_pydantic


@router.get('/games', response_model=list[game_pydantic_out])
async def list_game(token: str = Query(...)) -> list[game_pydantic_out]:
    games = await get_game_list()
    games_pydantic: list[game_pydantic_out] = [await game_pydantic_out.from_tortoise_orm(game) async for game in games]

    return games_pydantic


@router.get('/themes', response_model=list[theme_pydantic_out])
async def list_theme(token: str = Query(...), game_id: int = Query(...)) -> list[theme_pydantic_out]:
    game = await get_game_by_id(game_id)
    themes_pydantic: list[theme_pydantic_out] = [await theme_pydantic_out.from_tortoise_orm(theme) async for theme in
                                                 game.themes]

    return themes_pydantic


@router.get('/questions', response_model=list[question_pydantic_out])
async def list_question(token: str = Query(...), theme_id: int = Query(...)) -> list[question_pydantic_out]:
    theme = await get_theme_by_id(theme_id)
    if theme is None:
        raise HTTPException(status_code=404,
                            detail='theme not found')

    questions_pydantic: list[question_pydantic_out] = [await question_pydantic_out.from_tortoise_orm(question) async for
                                                       question in theme.questions]

    return questions_pydantic


@router.get('/questions/{theme_id}', response_model=question_pydantic_out)
async def get_question(token: str = Query(...), theme_id: int = Path(...), cost: int = Query(...)) -> question_pydantic_out:
    theme = await get_theme_by_id(theme_id)
    question = await theme.questions.filter(cost=cost)
    question_pydantic = await question_pydantic_out.from_tortoise_orm(question)

    return question_pydantic


@router.get('/answers/{question_id}', response_model=answer_pydantic_out)
async def get_answer(token: str = Query(...), question_id: int = Path(...)) -> answer_pydantic_out:
    question = await get_question_by_id(question_id)
    answer = await get_answer_by_question(question)
    answer_pydantic = await answer_pydantic_out.from_tortoise_orm(answer)

    return answer_pydantic
