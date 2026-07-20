"""FastAPI integration utilities for UFaaS."""

from fastapi import Request
from fastapi.responses import JSONResponse

from ..exceptions import UFaaSError


def ufaas_exception_handler(request: Request, exc: UFaaSError) -> JSONResponse:
    """Handle UFaaS exceptions."""

    if request.headers.get("accept-language"):
        locales = request.headers.get("accept-language").split(",")
        msg = {}
        for locale in locales:
            lang = locale.split("-")[0]
            if lang in exc.message:
                msg[lang] = exc.message.get(lang)
        message = msg
    else:
        message = exc.message

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": message,
            "error_code": exc.error_code,
            "detail": exc.detail,
            **exc.data,
        },
    )


EXCEPTION_HANDLERS = {UFaaSError: ufaas_exception_handler}
