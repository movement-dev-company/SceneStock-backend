import secrets

from fastapi.exceptions import HTTPException
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from core.config import settings
from core.database import get_db
from core.hashing import verify_password
from users.models import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request, db=next(get_db())) -> bool:
        form = await request.form()
        username, password = form.get('username'), form.get('password')

        user = db.query(User).filter(User.username == username).first()

        if not user:
            return False
        if not verify_password(password, user.password):
            return False

        if user.is_superuser or user.is_admin:
            token = secrets.token_urlsafe(64)
            request.session.update({'token': token})
            return True

        raise HTTPException(
            status_code=403,
            detail='Недостаточно прав для входа'
        )

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False
        return True


authentication_backend = AdminAuth(
    secret_key=settings.SECRET_KEY
)
