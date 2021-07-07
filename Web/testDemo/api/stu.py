from fastapi import APIRouter, Query

from pydantic import BaseModel

# 构建api路由
router = APIRouter()

from testDemo.service import userService


class Res(BaseModel):
    code: str = ""
    msg: str = ""
    data: dict = {}


@router.get("/show", tags=["users"], response_model=Res)
async def show():
    tmp = userService.showUser()
    msg = tmp[0];
    con = tmp[1]
    res = dict()
    res.update({"code": "1"})
    res.update({"msg": msg})
    res.update({"data": con})
    return res


@router.get("/add", tags=["users"], response_model=Res)
async def add(id: str, name: str, age: int = Query(..., ge=0, le=150)):
    msg = userService.addUser(id, name, age)
    res = dict()
    res.update({"code": "2"})
    res.update({"msg": msg})
    res.update({"data": {}})
    return res


@router.get("/delete", tags=["users"], response_model=Res)
async def delete(id: str):
    msg = userService.deleteUser(id)
    res = dict()
    res.update({"code": "3"})
    res.update({"msg": msg})
    res.update({"data": {}})
    return res


@router.get("/edit", tags=["users"], response_model=Res)
async def edit(id: str, name: str, age: int = Query(..., ge=0, le=150)):
    msg = userService.editUser(id, name, age)
    res = dict()
    res.update({"code": "4"})
    res.update({"msg": msg})
    res.update({"data": {}})
    return res
