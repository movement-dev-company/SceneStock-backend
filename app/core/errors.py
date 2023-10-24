from fastapi import Request, status, HTTPException, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


error_msg_templates = {
    'value_error.email': ['Введите корректный адрес электронной почты'],
    'value_error.missing': ['Обязательное поле'],
    'type_error.none.not_allowed': ['Значение не должно быть пустым'],
    'type_error.none.not_null': ['Значение не может быть пустым'],
}


def exception_handler(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ):
        errors = {}
        for exc in exc.errors():
            if exc.get('type') in error_msg_templates.keys():
                exc['msg'] = error_msg_templates[exc.get('type')]
            field = exc.get('loc')[1]
            error = exc.get('msg', [])
            if isinstance(error, str):
                error = [msg.strip(" '[]") for msg in error.split(',')]
            errors[field] = errors.get(field, []) + error
        return JSONResponse(
            content=errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    @app.exception_handler(HTTPException)
    def http_exception_handler(_: Request, exc: HTTPException):
        return JSONResponse(
            content=exc.detail,
            status_code=exc.status_code
        )
