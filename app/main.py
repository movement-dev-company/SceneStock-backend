import uvicorn
from fastapi import FastAPI

from const import API_URL
from core.database import Base, engine
from core.errors import exception_handler
from tags.router import router_tags
from users.router import router_auth, router_user
from users.auth import router_token


app = FastAPI(arbitrary_types_allowed=True, debug=True)
Base.metadata.create_all(bind=engine)


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
exception_handler(app)


@app.get('/',)
def index():
    return {'data': {'name': 'Its base!'}}


def main():
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
