from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse

from config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        if not username or not password:
            return False

        if username == settings.ADMIN_USERNAME_BACKEND and password == settings.ADMIN_PASSWORD_BACKEND:
            request.session["user"] = username
            return True

        return False

    async def authenticate(self, request: Request):
        user = request.session.get("user")

        if user is None:
            return RedirectResponse(url="/admin/login")

        return user

    async def logout(self, request: Request):
        request.session.pop("user", None)
        return RedirectResponse(url="/admin/login")
