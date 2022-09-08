from functools import wraps


def login_required(target: str, attribute: str) -> callable:
    def wrapper(function: callable) -> callable:
        @wraps(function)
        async def wrapped(*args: object, **kwargs: object) -> object:
            kwargs.get(target).__getattribute__(attribute)()

            return await function(*args, **kwargs)
        return wrapped
    return wrapper
