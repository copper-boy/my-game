from tortoise.queryset import QuerySet

from app.orm.game import AnswerModel, GameModel, QuestionModel, ThemeModel


async def create_answer(correct: str, question: QuestionModel) -> AnswerModel:
    answer = await AnswerModel.create(correct=correct, question=question)
    return answer


async def get_answer_by_question(question: QuestionModel) -> AnswerModel:
    answer = await AnswerModel.get_or_none(question=question)
    return answer


async def create_game(name: str) -> GameModel:
    game = await GameModel.create(name=name)
    return game


async def get_game_by_id(id: int) -> GameModel:
    game = await GameModel.get_or_none(id=id)
    return game


async def get_game_by_name(name: str) -> GameModel:
    game = await GameModel.get_or_none(name=name)
    return game


async def get_games_count() -> int:
    return GameModel.all().count()


async def get_games_list(offset: int) -> QuerySet[GameModel]:
    games = await GameModel.all().offset(offset)
    return games


async def get_themes_count(game: GameModel) -> ThemeModel:
    return await ThemeModel.filter(game=game).count()


async def get_themes_list(game: GameModel, offset: int) -> QuerySet[ThemeModel]:
    themes = await ThemeModel.filter(game=game).offset(offset)
    return themes


async def create_theme(title: str, game: GameModel) -> ThemeModel:
    theme = await ThemeModel.create(title=title, game=game)

    return theme


async def get_theme_by_id(id: int) -> ThemeModel:
    theme = await ThemeModel.get_or_none(id=id)
    return theme


async def create_question(title: str, cost: int, theme: ThemeModel) -> QuestionModel:
    question = await QuestionModel.create(title=title, cost=cost, theme=theme)
    return question


async def get_question_by_id(id: int) -> QuestionModel:
    question = await QuestionModel.get_or_none(id=id)
    return question


async def get_questions_count(theme_id: int) -> int:
    return await QuestionModel.filter(theme_id=theme_id).count()
