import uvicorn
from fastapi import FastAPI

from core.database import Base, engine
from users.router import router_auth
from core.errors import exception_handler


app = FastAPI(arbitrary_types_allowed=True, debug=True)
Base.metadata.create_all(bind=engine)


app.include_router(router_auth, prefix='/auth', tags=['Authentication'],)
exception_handler(app)


@app.get('/',)
def index():
    return {'data': {'name': 'Its base!'}}


def main():
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
