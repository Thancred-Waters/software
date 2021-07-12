from fastapi import status
from fastapi.responses import JSONResponse, Response  # , ORJSONResponse
from typing import Union

# 注意有个 * 号 不是笔误， 意思是调用的时候要指定参数 e.g.resp_200（data=xxxx)
def resp_200(*, data: Union[list, dict, str]) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 200,
            'message': "Success",
            'data': data,
        }
    )
    
def resp_400(*, data: str = None, message: str="BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'message': message,
            'data': data,
        }
    )
