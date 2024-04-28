import traceback

from fastapi import HTTPException, Request, Response
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.api.common.errors import APIException
from app.api.common.errors.response import (
    make_api_exception_response,
    make_internal_error_response,
    make_param_invalid_response,
)
from app.seedwork.domain.exception import ApplicationException
from app.utils.logger import get_logger

logger = get_logger()


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
        except ValidationError as e:
            logger.error(e)
            return make_param_invalid_response()
        except (APIException, ApplicationException) as e:
            logger.error(e)
            return make_api_exception_response(e)
        except HTTPException as e:
            logger.error(e)
            traceback.print_exc()
            return make_internal_error_response()
        except Exception as e:
            logger.error(e)
            traceback.print_exc()
            # todo: alert
            return make_internal_error_response()

        return response
