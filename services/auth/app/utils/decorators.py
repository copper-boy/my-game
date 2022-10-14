from functools import wraps


def login_required(target: str, attribute: str, *d_args, **d_kwargs) -> callable:
    def wrapper(function: callable) -> callable:
        @wraps(function)
        async def wrapped(*f_args: object, **f_kwargs: object) -> object:
            f_kwargs.get(target).__getattribute__(attribute)(*d_args, **d_kwargs)

            return await function(*f_args, **f_kwargs)
        return wrapped
    return wrapper
