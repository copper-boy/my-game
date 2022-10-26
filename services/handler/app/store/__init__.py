from aiohttp.web import Application

from app.settings.config import get_telegram_bot_settings


class Store:
    def __init__(self, application: Application) -> None:
        from app.store.aiohttp_session.accessor import AiohttpSessionAccessor
        from app.store.bot.accessor import BotAccessor
        from app.store.game_state.accessor import GameStateAccessor
        from app.store.player.accessor import PlayerAccessor
        from app.store.question_session.accessor import QuestionSessionAccessor
        from app.store.session.accessor import SessionAccessor

        self.aiohttp_session_accessor = AiohttpSessionAccessor(application=application)
        self.bot_accessor = BotAccessor(application=application, bot_token=get_telegram_bot_settings().TELEGRAM_BOT_API_TOKEN)
        self.game_states = GameStateAccessor(application)
        self.players = PlayerAccessor(application)
        self.questions_sessions = QuestionSessionAccessor(application)
        self.sessions = SessionAccessor(application)


def setup_store(app: Application) -> None:
    from app.store.database.database import Database

    app.database = Database(app)

    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)

    app.store = Store(app)
