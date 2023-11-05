import argparse

import uvicorn
from fastapi import FastAPI

from admin.admin import AdminManager
from admin.admin_models import TagAdmin, UserAdmin
from admin.auth import authentication_backend
from const import API_URL
from core.database import Base, engine
from core.db_utils import create_superuser
from core.errors import exception_handler
from tags.router import router_tags
from users.auth import router_token
from users.router import router_auth, router_user

app = FastAPI(arbitrary_types_allowed=True, debug=True)
Base.metadata.create_all(bind=engine)

exception_handler(app)

admin = AdminManager(
    app, engine, title='SceneStock Admin',
    authentication_backend=authentication_backend
)
admin.add_db_models((UserAdmin, TagAdmin, FastAPI))

app.include_router(
    router_auth, prefix=f'{API_URL}/auth', tags=['Authentication'],
)
app.include_router(
    router_tags, prefix=f'{API_URL}/tags', tags=['Tags'],
)
app.include_router(
    router_token, prefix=f'{API_URL}/auth', tags=['Token'],
)
app.include_router(
    router_user, prefix=f'{API_URL}/users', tags=['User'],
)


@app.get('/',)
def index():
    return {'data': {'name': 'Its base!'}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'create_superuser', type=str, nargs='?',
        help='Create user with superuser role'
    )
    parser.add_argument(
        '--host', default='127.0.0.1', help='Host IP address for the server'
    )
    parser.add_argument(
        '--port', type=int, default=8000, help='Port for the server'
    )
    args = parser.parse_args()

    if args.create_superuser == 'create_superuser':
        print(create_superuser())
    else:
        uvicorn.run(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
