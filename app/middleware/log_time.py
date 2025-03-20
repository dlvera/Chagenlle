from fastapi import Request
import time
import logging
from typing import Callable, Awaitable

logger = logging.getLogger("request_logger")

class ResponseTimeLogger:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        start_time = time.time()
        request = Request(scope)
        status_code = 500  # Valor por defecto

        # Capturamos el código de estado del primer mensaje de respuesta
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"{request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status": status_code,
                    "time_ms": round(process_time, 2)
                }
            )