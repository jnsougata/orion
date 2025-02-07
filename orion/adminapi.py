from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response

from .authentication import authenticate
from .dashboard import DASHBOARD
from .login import LOGIN_PAGE
from .utils import adminonly


@adminonly
async def list_bases(request: Request):
    return JSONResponse(content={"bases": request.app.database.list_all()})


@adminonly
async def list_tables(request: Request):
    base = request.path_params.get("base")
    if base is None:
        return JSONResponse(content={"message": "No base specified!"}, status_code=400)
    return JSONResponse(content={"tables": request.app.database.list_tables(base)})


@adminonly
async def table_to_json(request: Request):
    base = request.path_params.get("base")
    table = request.path_params.get("table")
    if base is None or table is None:
        return JSONResponse(
            content={"message": "No base or table specified!"}, status_code=400
        )
    return JSONResponse(content=request.app.database.table_to_dict(base, table))


async def admin_login(request: Request):
    if request.method == "GET":
        return HTMLResponse(LOGIN_PAGE)
    if request.method == "POST":
        auth = await authenticate(
            request,
            database="admin.db",
            table="admins",
            header_name="X-Authorization-Token",
        )
        if not auth:
            return Response(
                content='{"message": "Login failed!"}',
                media_type="application/json",
                status_code=401,
            )
        headers = {"Set-Cookie": f"Authorization={auth}"}
        return JSONResponse(content='{"message": "Login successful!"}', headers=headers)


async def admin_dashboard(request: Request):
    auth = await authenticate(
        request, database="admin.db", table="admins", header_name="Cookie"
    )
    if not auth:
        return Response(
            content='{"message": "Login failed!"}', media_type="application/json"
        )
    return HTMLResponse(DASHBOARD)


def load_admin_routes(app: Starlette):
    app.add_route("/admin/login", admin_login, methods=["GET", "POST"])
    app.add_route("/admin/dashboard", admin_dashboard, methods=["GET"])
    app.add_route("/admin/api/bases", list_bases, methods=["GET"])
    app.add_route("/admin/api/bases/{base}", list_tables, methods=["GET"])
    app.add_route(
        "/admin/api/bases/{base}/tables/{table}", table_to_json, methods=["GET"]
    )
