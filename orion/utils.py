import hmac

from starlette.requests import Request
from starlette.responses import JSONResponse

from .authentication import authenticate


def adminonly(coro):
    async def wrapper(request: Request, *args, **kwargs):
        auth = await authenticate(
            request, database="admin.db", table="admins", header_name="Cookie"
        )
        if not auth:
            return JSONResponse(content={"message": "Unauthorized"}, status_code=401)
        return await coro(request, *args, **kwargs)

    return wrapper
