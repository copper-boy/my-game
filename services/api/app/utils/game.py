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


async def get_game_list() -> QuerySet[GameModel]:
    games = GameModel.all()
    return games


async def create_theme(title: str, game: GameModel) -> ThemeModel:
    theme = await ThemeModel.create(title=title, game=game)

    return theme


async def get_theme_by_id(id: int) -> ThemeModel:
    theme = await ThemeModel.get_or_none(id=id)
    return theme


async def create_question(title: str, cost: int, theme: ThemeModel) -> QuestionModel:
    question = await QuestionModel.create(title=title, cost=cost, theme=theme)
    return question


async def get_question_by_id(id: int) -> AnswerModel:
    answer = await QuestionModel.get_or_none(id=id)
    return answer
