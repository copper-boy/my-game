from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Path, Query

from app.orm.game import (answer_pydantic_in, answer_pydantic_out,
                          game_pydantic_in, game_pydantic_out,
                          question_pydantic_in, question_pydantic_out,
                          theme_pydantic_in, theme_pydantic_out)
from app.utils.game import (create_answer, create_game, create_question,
                            create_theme, get_answer_by_question,
                            get_game_by_id, get_game_by_name, get_games_count,
                            get_games_list, get_question_by_id,
                            get_questions_count, get_theme_by_id,
                            get_themes_list)

router = APIRouter()


@router.post('/answer', response_model=answer_pydantic_out)
async def post_answer(data: answer_pydantic_in, question_id: int = Query(...),
                      token: str = Query(...)) -> answer_pydantic_out:
    question = await get_question_by_id(question_id)
    if await get_answer_by_question(question):
        raise HTTPException(status_code=409,
                            detail='answer already exists')

    answer = await create_answer(correct=data.correct, question=question)
    answer_pydantic = await answer_pydantic_out.from_tortoise_orm(answer)

    return answer_pydantic


@router.post('/game', response_model=game_pydantic_out)
async def post_game(data: game_pydantic_in, token: str = Query(...)) -> game_pydantic_out:
    if await get_game_by_name(data.name) is not None:
        raise HTTPException(status_code=409,
                            detail='game already exists')

    game = await create_game(**data.dict())
    game_pydantic = await game_pydantic_out.from_tortoise_orm(game)

    return game_pydantic


@router.post('/theme', response_model=theme_pydantic_out)
async def post_theme(data: theme_pydantic_in,
                     token: str = Query(...),
                     game_id: int = Query(...)) -> theme_pydantic_out:
    game = await get_game_by_id(game_id)
    if game is None:
        raise HTTPException(status_code=404,
                            detail='game not found')

    if await game.themes.filter(title=data.title).first():
        raise HTTPException(status_code=409,
                            detail='theme already exists')

    theme = await create_theme(**data.dict(), game=game)
    theme_pydantic = await theme_pydantic_out.from_tortoise_orm(theme)

    return theme_pydantic


@router.post('/question', response_model=question_pydantic_out)
async def post_question(data: question_pydantic_in,
                        token: str = Query(...),
                        theme_id: int = Query(...)) -> question_pydantic_out:
    theme = await get_theme_by_id(theme_id)
    if theme is None:
        raise HTTPException(status_code=404,
                            detail='theme not found')

    question = await create_question(**data.dict(), theme=theme)
    question_pydantic = await question_pydantic_out.from_tortoise_orm(question)

    return question_pydantic


@router.get('/games/{game_id}', response_model=game_pydantic_out)
async def get_game(token: str = Query(...),
                   game_id: int = Path(...)) -> game_pydantic_out:
    game = await get_game_by_id(game_id)
    if game is None:
        raise HTTPException(status_code=404,
                            detail='game not found')

    game_pydantic = await game_pydantic_out.from_tortoise_orm(game)

    return game_pydantic


@router.get('/count/games')
async def count_games(token: str = Query(...)) -> dict:
    count = await get_games_count()

    return {'count': count}


@router.get('/games', response_model=list[game_pydantic_out])
async def list_game(token: str = Query(...),
                    offset: int = Query(default=0)) -> list[game_pydantic_out]:
    games = await get_games_list(offset=offset)
    games_pydantic: list[game_pydantic_out] = [await game_pydantic_out.from_tortoise_orm(game) for game in games]

    return games_pydantic


@router.get('/themes', response_model=list[theme_pydantic_out])
async def list_theme(token: str = Query(...),
                     game_id: int = Query(...)) -> list[theme_pydantic_out]:
    game = await get_game_by_id(id=game_id)
    if game is None:
        raise HTTPException(status_code=404,
                            detail='game not found')

    themes = await get_themes_list(game=game)
    themes_pydantic: list[theme_pydantic_out] = [await theme_pydantic_out.from_tortoise_orm(theme) for theme in themes]

    return themes_pydantic


@router.get('/themes/{theme_id}', response_model=theme_pydantic_out)
async def get_theme(token: str = Query(...),
                    theme_id: int = Path(...)) -> theme_pydantic_out:
    theme = await get_theme_by_id(theme_id)
    if theme is None:
        raise HTTPException(status_code=404,
                            detail='theme not found')

    theme_pydantic = await theme_pydantic_out.from_tortoise_orm(theme)

    return theme_pydantic


@router.get('/questions', response_model=list[question_pydantic_out])
async def list_question(token: str = Query(...),
                        theme_id: int = Query(...)) -> list[question_pydantic_out]:
    theme = await get_theme_by_id(theme_id)
    if theme is None:
        raise HTTPException(status_code=404,
                            detail='theme not found')

    questions_pydantic: list[question_pydantic_out] = [await question_pydantic_out.from_tortoise_orm(question) async for
                                                       question in theme.questions]

    return questions_pydantic


@router.get('/count/questions')
async def count_questions(token: str = Query(...),
                          theme_id: int = Query(...)) -> dict:
    count = await get_questions_count(theme_id)
    return {'count': count}


@router.get('/questions/{question_id}', response_model=question_pydantic_out)
async def get_question(token: str = Query(...),
                       question_id: int = Path(...)) -> question_pydantic_out:
    question = await get_question_by_id(question_id)
    if question is None:
        raise HTTPException(status_code=404,
                            detail='question not found')

    question_pydantic = await question_pydantic_out.from_tortoise_orm(question)

    return question_pydantic


@router.get('/answers/{question_id}', response_model=answer_pydantic_out)
async def get_answer(token: str = Query(...),
                     question_id: int = Path(...)) -> answer_pydantic_out:
    question = await get_question_by_id(question_id)
    if question is None:
        raise HTTPException(status_code=404,
                            detail='question not found')

    answer = await get_answer_by_question(question)
    if answer is None:
        raise HTTPException(status_code=404,
                            detail='answer not found')

    answer_pydantic = await answer_pydantic_out.from_tortoise_orm(answer)

    return answer_pydantic
