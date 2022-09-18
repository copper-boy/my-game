from aiohttp.web import Application


class Store:
    def __init__(self, application: Application) -> None:
        from app.store.game_state.accessor import GameStateAccessor
        from app.store.player.accessor import PlayerAccessor
        from app.store.question_session.accessor import QuestionSessionAccessor
        from app.store.session.accessor import SessionAccessor

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
