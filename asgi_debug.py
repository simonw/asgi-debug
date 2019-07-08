from pprint import pformat
from functools import wraps


def asgi_debug_decorator(log_to=print):
    def _asgi_debug_decorator(app):
        @wraps(app)
        async def app_wrapped_with_debug(scope, recieve, send):
            log_to(pformat(scope))
            log_to("\n")
            async def wrapped_send(event):
                log_to(pformat(event))
                log_to("\n")
                await send(event)

            async def wrapped_recieve(event):
                log_to(pformat(event))
                log_to("\n")
                await recieve(event)

            await app(scope, wrapped_recieve, wrapped_send)

        return app_wrapped_with_debug

    return _asgi_debug_decorator


def asgi_debug(app, log_to=print):
    return asgi_debug_decorator(log_to=log_to)(app)
