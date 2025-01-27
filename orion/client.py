import hashlib
import os
import re
from typing import Any, Dict, Optional

import jinja2
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from .adminapi import attach_admin_routes
from .database import Database
from .enums import DBScope, UseAuthBool
from .renderer import Tree


class _View:
    def __init__(
        self,
        *,
        file_path: str,
        route: str,
        use_auth: UseAuthBool = UseAuthBool.FALSE,
        db_scope: DBScope = DBScope.READONLY,
        method: Optional[str] = None,
    ):
        self.file_path = file_path
        self.route = route
        self.use_auth = use_auth
        self.db_scope = db_scope
        self.methods = method or "GET"


class Orion(Starlette):
    def __init__(
        self,
        views_dir: str = "views",
        public_dir: str = "public",
        database_dir: str = ".database",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.superuser = None
        self.password = None
        self.views_dir = views_dir
        self.public_dir = public_dir
        self.database = Database(database_dir)
        self.connections = self.database.fetch_all()
        self.__jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.views_dir)
        )
        self._view_map: Dict[str, _View] = {}
        self._attach_views()
        self.mount("/public", StaticFiles(directory=self.public_dir), name="public")
        attach_admin_routes(self)

    def create_admin(
        self,
        *,
        username: str,
        password: str,
        name: str,
        email: str,
        access_level: int = 0,
    ):
        con = self.database.connect("admin.db")
        self.connections["admin.db"] = con
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                access_level INTEGER DEFAULT 0,
                password TEXT NOT NULL,
                UNIQUE(username),
                CHECK(LENGTH(username) > 0),
                CHECK(LENGTH(password) > 8),
                CHECK(LENGTH(username) < 100)
            )
            """
        )
        hashed = hashlib.sha256(password.encode(), usedforsecurity=True).hexdigest()
        con.execute(
            "INSERT INTO admins (username, name, email, access_level, password) VALUES (?, ?, ?, ?, ?)",
            (username, name, email, access_level, hashed),
        )
        con.commit()
        return con

    @staticmethod
    def __build_matched_raw_route(request: Request):
        params = request.path_params
        path = request.url.path
        for key, value in params.items():
            path = path.replace(value, f"{{{key}}}")
        return path

    @staticmethod
    def __parse_config(html: str) -> Dict[str, Any]:
        pattern = r"<!--<cfg>(.*?)</cfg>-->"
        conf = {}
        matched = re.search(pattern, html, re.DOTALL)
        if not matched:
            return conf
        conf_str = matched.group(1)
        for pair in conf_str.split(","):
            key, value = pair.split(":")
            conf[key.strip()] = value.strip()
        return conf

    async def _handler(self, request: Request, *args, **kwargs):
        view = self._view_map[self.__build_matched_raw_route(request)]
        with Tree(f"{self.views_dir}/{view.file_path}") as tree:
            template = jinja2.Template(str(tree))
            template = template.render(request=request, view=view, *args, **kwargs)
            return HTMLResponse(content=template)

    def _attach_views(self):
        for root, dirs, files in os.walk(self.views_dir):
            for file in files:
                if file.endswith(".html"):
                    path = os.path.join(root, file)
                    with open(path, "r") as f:
                        route = f"{path}"[:-5].replace(self.views_dir, "")
                        if route == "/index":
                            route = "/"
                        config = self.__parse_config(f.read())
                        view = _View(
                            file_path=path.replace(self.views_dir, "")[1:],
                            route=route,
                            use_auth=UseAuthBool(config.get("use_auth", "false")),
                            db_scope=DBScope(int(config.get("db_scope", "1"))),
                            method=config.get("method"),
                        )
                        self._view_map[route] = view
                        self.add_route(route, self._handler)

    def run(self, host: str = "localhost", port: int = 8000, *args, **kwargs):
        uvicorn.run(self, host=host, port=port, *args, **kwargs)

    def on_startup(self):

        def wrapper(coro):
            self.add_event_handler("startup", coro)
        return wrapper

    def on_shutdown(self):

        def wrapper(coro):

            async def handler():
                await coro()
                for con in self.connections.values():
                    con.close()

            self.add_event_handler("shutdown", handler)
        return wrapper
