import hmac

from starlette.requests import Request


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
