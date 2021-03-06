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
    """
    
    处理用户登录请求，不允许重复登录，且后厨同一时间只有一个账户能够登录
    Parameters
    ----------
    user : UserIn
        用户信息.

    Returns
    -------
    res : TYPE
        登录结果.

    """
    msg,data=loginService.login(user.name,user.password)
    res=dict({'code':1})
    res.update({'msg':msg})
    res.update({'data':data})
    return res