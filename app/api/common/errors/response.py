from typing import Optional

from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.api.common.errors import APIException
from app.seedwork.domain.exception import ApplicationException


class ExceptionResponse(BaseModel):
    err_details: str = ""
    err_code: str = ""
    err_msg: str = ""
    status_code: int = 0
    data: Optional[dict]


def make_internal_error_response():
    content = {"err_details": "", "err_code": "990001", "err_msg": "内部错误", "status_code": 0}
    return JSONResponse(content, status_code=200)


def make_param_invalid_response() -> JSONResponse:
    content = {"err_details": "", "err_code": "100001", "err_msg": "参数错误", "status_code": 0}
    return JSONResponse(content, status_code=200)


def make_api_exception_response(api_exception: APIException | ApplicationException) -> JSONResponse:
    response = ExceptionResponse(
        err_details=api_exception.err_details,
        err_code=api_exception.err_code,
        err_msg=api_exception.err_msg,
        status_code=api_exception.status_code,
    )
    if hasattr(api_exception, "data"):
        response.data = api_exception.data
    return JSONResponse(response.dict(), status_code=200)
