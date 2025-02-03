import hmac
from abc import ABCMeta

from starlette.requests import Request
from typing_extensions import Protocol


async def authenticate(
    request: Request, *, header_name: str, database: str, table: str
):
    if header_name not in request.headers:
        return
    auth = request.headers[header_name]
    if header_name == "Cookie":
        auth = request.cookies.get("Authorization")
    username, hashed = auth.split(":")
    con = request.app.connections[database]
    cursor = con.cursor()
    cursor.execute(f"SELECT password FROM {table} WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        return
    ok = hmac.compare_digest(hashed, result[0])
    if not ok:
        return
    return auth


class AuthenticationProvider(Protocol):
    async def authenticate(self, request: Request):
        ...

    async def verify_cookie(self, request: Request):
        ...

    async def login(self, request: Request):
        ...

    async def logout(self, request: Request):
        ...

    async def register(self, request: Request):
        ...

    async def change_password(self, request: Request):
        ...

    async def reset_password(self, request: Request):
        ...

    async def delete_account(self, request: Request):
        ...

    async def verify_email(self, request: Request):
        ...

    async def change_email(self, request: Request):
        ...