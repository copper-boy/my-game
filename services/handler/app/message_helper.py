class MessageHelper:
    def __init__(self) -> None:
        ...

    @staticmethod
    def bad_message(username: str) -> str:
        return f'@{username}, the bot cannot complete your action!'
