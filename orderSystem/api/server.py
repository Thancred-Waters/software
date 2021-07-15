# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 19:28:12 2021

@author: zc
"""

from fastapi import APIRouter,Body

from pydantic import BaseModel

from datetime import datetime

from typing import List

from orderSystem.service import serverService

# 构建api路由
router = APIRouter()

class Order_Pre(BaseModel) :
    #服务员发送的菜品订单
    table:int = 0
    id:int = 0
    num:int = 0
    order:dict = {}#菜品详细信息，{菜名:数量}
    
class Order_After(BaseModel) :
    #后台确认的菜品订单
    订单编号:str = ""
    下单时间:datetime = datetime(2000,1,1)
    菜品列表:dict = {}#菜品详细信息，{菜名:数量}
    
class Table_Order(BaseModel) :
    #每桌下的订单
    桌号:str = ""
    下单时间:datetime = datetime(2000,1,1)
    金额:float = 0
    人数:int = 0
    订单状态:str = ""
    订单内容:list = []
    菜品总数:int = 0

class BuyOrder(BaseModel) :
    桌号:int = 0
    人数:int = 0
    金额:float = 0
    订单编号:str = ""
    
class Broadcast(BaseModel) :
    标题:str = ""
    时间:datetime = datetime(2000,1,1)
    内容:str = ""  
    
class Res(BaseModel) :
    #基础返回模型
    code:int = 0
    msg:str = ""
    
class ResOrder(Res) :
    #返回下单状态列表
    data:Order_After = Order_After()
    
class ResBroad(Res) :
    #返回广播请求列表
    data:List[Broadcast] = list()  
    
class ResTableOrder(Res) :
    #返回所有订单列表
    data:List[Table_Order] = list()
    
class ResBuyOrder(Res) :
    #返回买单请求状态
    data:BuyOrder = BuyOrder()
    
class ResPass(Res) :
    data:dict = {}
    
class ResMenu(Res) :
    data:List[dict] = list()

@router.post('/place_order',response_model=ResOrder)
async def place_order(order:Order_Pre) :
    """
    服务员下单

    Parameters
    ----------
    order : Order_Pre
        下单订单.

    Returns
    -------
    res : TYPE
        下单状态.

    """
    msg,data=serverService.place_order(order.table, order.id, 
                                       order.num, order.order)
    res = ResOrder()
    res.msg = msg
    res.data = data
    return res

@router.get("/window",response_model=ResBroad)
async def window() :
    """
    获取未被展示的最新公告

    Returns
    -------
    res : TYPE
        弹窗公告.

    """
    #发送弹窗公告
    msg,data=serverService.window()
    res=ResBroad()
    res.msg=msg
    res.data=data
    return res

@router.post("/broadcast",response_model=ResBroad)
async def broadcast(id:int = Body(...,embed=True)) :
    """
    获取最近公告

    Returns
    -------
    res : TYPE
        公告列表.

    """
    #发送驻留公告
    msg,data=serverService.broadcast(id)
    res=ResBroad()
    res.msg=msg
    res.data=data
    return res

@router.post("/show",response_model=ResTableOrder)
async def show(id:int = Body(...,embed=True)) :
    """
    
    展示所有订单
    Returns
    -------
    res : TYPE
        所有订单状态.

    """
    msg,data = serverService.show(id)
    res=ResTableOrder()
    res.msg=msg
    res.data=data
    return res

@router.post("/buy",response_model=ResBuyOrder)
async def buy(table:int = Body(...,embed=True),
              id:int = Body(...,embed=True)) :
    """
    
    服务员发送买单请求
    Parameters
    ----------
    table : int, optional
        桌号. The default is Body(...,embed=True).
    id : int, optional
        服务员编号. The default is Body(...,embed=True).

    Returns
    -------
    res : TYPE
        买单请求结果.

    """
    msg=serverService.buy(table, id)
    res=ResBuyOrder()
    res.msg=msg
    return res

@router.post("/logout",response_model=Res)
async def logout(id:int = Body(...,embed=True)) :
    """
    服务员登出

    Parameters
    ----------
    id : int, optional
        服务员工号. The default is Body(...,embed=True).

    Returns
    -------
    res : TYPE
        登出请求是否成功.

    """
    msg=serverService.logout(id)
    res=Res()
    res.msg=msg
    return res

@router.post("/pass",response_model=ResPass)
async def pass_order(id:int = Body(...,embed=True)) :
    """
    服务员发送传菜请求

    Returns
    -------
    None.

    """
    msg,data=serverService.pass_order(id)
    res=ResPass()
    res.msg=msg
    res.data=data
    return res

@router.post("/query_menu",response_model=ResMenu)
async def query_menu(id:int = Body(...,embed=True)) :
    msg,data=serverService.query_menu(id)
    res=ResMenu()
    res.msg=msg
    res.data=data
    return res

@router.post("/pass_dish", response_model=Res)
async def pass_dish(id: int = Body(...,embed=True), 
                    table: int = Body(...,embed=True), 
                    name: str = Body(...,embed=True)):
    """
    :param id: 员工id号
    :param table: 订单卓号
    :param name: 被传递的菜品名称
    :return: 处理是否成功
    """
    msg = serverService.pass_dish(id,table,name)
    res = Res()
    res.msg = msg
    res.code = 20
    return res
