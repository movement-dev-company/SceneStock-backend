from typing import List, Sequence

from sqladmin import Admin
from sqladmin._types import ENGINE_TYPE
from sqladmin.authentication import AuthenticationBackend
from sqladmin.models import ModelViewMeta
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm.session import sessionmaker
from starlette.applications import Starlette
from starlette.middleware import Middleware


class AdminManager(Admin):
    """
    Custom administrative interface manager for web applications.

    This class extends the functionality of the `Admin` class, allowing you
    to manage and configure the administrative interface for your web
    application.

    The `AdminManager` class allows you to add database models and customize
    the administrative interface of your web application.
    """

    def __init__(
        self,
        app: Starlette,
        engine: ENGINE_TYPE | None = None,
        session_maker: sessionmaker | async_sessionmaker | None = None,
        base_url: str = "/admin",
        title: str = "Admin",
        logo_url: str | None = None,
        middlewares: Sequence[Middleware] | None = None,
        debug: bool = False,
        templates_dir: str = "templates",
        authentication_backend: AuthenticationBackend | None = None
    ) -> None:
        super().__init__(
            app,
            engine,
            session_maker,
            base_url,
            title,
            logo_url,
            middlewares,
            debug,
            templates_dir,
            authentication_backend
        )

    def add_db_models(self, models: List[ModelViewMeta]):
        """
        Adds models to the administrative interface.

        :param models: List of ModelViewMeta instances representing models
        to be administered.
        """

        for model in models:
            if not isinstance(model, ModelViewMeta):
                raise ValueError(
                    f'Model {model.__name__} must be an instance of ModelView.'
                )
            self.add_view(model)
