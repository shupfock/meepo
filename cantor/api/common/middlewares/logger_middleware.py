import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from cantor.utils.logger import get_logger

logger = get_logger()


class LoggerHandleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        st = time.time()
        resp = await call_next(request)
        delta_t = time.time() - st
        logger.info(f"[{resp.status_code}] Time took to process the {request.url} and return response is {delta_t} sec")
        # todo alter
        return resp
