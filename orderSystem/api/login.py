# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 19:32:01 2021

@author: zc
"""

from orderSystem.service import loginService

from fastapi import APIRouter

from pydantic import BaseModel
from typing import Optional

router=APIRouter()

class UserIn(BaseModel) :
    #用户登陆消息体
    name:str
    password:str
    code1:Optional[str] = ""
    code2:Optional[str] = ""
    
class User(BaseModel) :
    id:int
    name:str
    job:int
    pic:str
    
class UserOut(BaseModel) :
    #用户登出消息体
    code:int
    msg:str
    data:User

@router.post("/",response_model=UserOut)
async def login(user : UserIn) :
    msg,data=loginService.login(user.name,user.password)
    res=dict({'code':1})
    res.update({'msg':msg})
    res.update({'data':data})
    return res