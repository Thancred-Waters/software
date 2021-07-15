# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 19:28:53 2021

@author: zc
"""

from fastapi import APIRouter,Body

from pydantic import BaseModel
from typing import List

from datetime import datetime

from orderSystem.service import cookService

# 构建api路由
router = APIRouter()

class Confirm(BaseModel) :
    #后厨确认接到菜品订单/后厨完成对应菜品的制作
    id:int = 0
    桌号:int = 0
    菜名:str = ""
    数量:int = 0
    负责人:str = ""

class Dish(BaseModel) :
    #每道菜的状态
    桌号:int = 0
    菜名:str = ""
    数量:int = 0
    状态:str = ""

class Broadcast(BaseModel) :
    标题:str = ""
    时间:str = ""
    内容:str = ""

class Res(BaseModel) :
    #基础返回模型
    code:int = 0
    msg:str = ""
    
class ResDish(Res) :
    #返回所有已下单菜的列表
    data:List[Dish] = list()
    
class ResConfirm(Res) :
    #确认/结束订单返回体
    data:Confirm = Confirm()
    
class ResBroad(Res) :
    data:List[Broadcast] = list()

@router.post("/show",response_model=ResDish)
async def show(id:int = Body(...,embed=True)) :
    #获取所有订单信息
    msg,data=cookService.show(id) 
    res=ResDish()
    res.code=9
    res.msg=msg
    res.data=data
    return res

@router.post("/confirm",response_model=ResConfirm)
async def confirm(con:Confirm) :
    #确认菜品订单已收到
    ans=cookService.confirm(con.id,con.桌号, con.菜名, con.数量)
    res=ResConfirm()
    res.code=10
    res.msg=ans
    res.data=con
    return res

@router.post("/finish",response_model=ResConfirm)
async def finish(con:Confirm) :
    #确认菜品订单已完成
    ans=cookService.finish(con.id,con.桌号, con.菜名, con.数量)
    res=ResConfirm()
    res.code=11
    res.msg=ans
    res.data=con
    return res

@router.get("/window",response_model=ResBroad)
async def window() :
    #发送弹窗公告
    ans,data=cookService.window()
    res=ResBroad()
    res.code=12
    res.msg=ans
    res.data=data
    return res

@router.post("/broadcast",response_model=ResBroad)
async def broadcast(id:int = Body(...,embed=True)) :
    #发送驻留公告
    ans,data=cookService.broadcast(id)
    res=ResBroad()
    res.code=13
    res.msg=ans
    res.data=data
    return res

@router.post('/logout',response_model=Res)
async def logout(id:int = Body(...,embed=True)) :
    #响应用户登出请求
    ans=cookService.logout(id)
    res=Res()
    res.code=14
    res.msg=ans
    return res

