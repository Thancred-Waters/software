# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 19:29:04 2021

@author: zc
"""

from fastapi import APIRouter,Body,UploadFile,File,Form

from pydantic import BaseModel

from typing import List,Optional

from orderSystem.service import adminService
# 构建api路由
router = APIRouter()

class Res(BaseModel) :
    code:int = 0
    msg:str = ""

class Modify_Content(BaseModel) :
    #管理员修改菜品请求体
    菜品id:int = 0
    菜名:str = ""
    价格:float = 0
    是否推荐:str = ""
    简介:str = ""
    图片:Optional[str] = ""

class Res_Modify(Res) :
    code:int = 0
    msg:str = ""
    data:Modify_Content = Modify_Content()
    
class Finish(BaseModel) :
    id:int = 0
    订单号:str = ""
    是否免单:str = ""
    结账金额:float = 0
    
class Res_Finish(Res) :
    data:dict = {}    
    
class Res_Show(Res) :
    data:List[dict] = list()
    
class Add_Menu(BaseModel) :
    id:int = 0
    菜名:str = ""
    价格:float = 0
    是否推荐:str = ""
    简介:str = ""
    图片:Optional[str] = ""
    
class Create_User(BaseModel) :
    管理员id:int = 0
    创建用户名:str = ""
    密码:str = ""
    确认密码:str = ""
    身份:str = ""
    图片:str = ""
    
@router.post('/modify',response_model=Res_Modify)
async def modify(mod:Modify_Content) :
    """
    
    管理员提交修改订单请求
    Parameters
    ----------
    mod : Modify_Content
        修改订单请求.

    Returns
    -------
    res : TYPE
        修改结果.

    """
    msg,data=adminService.modify(*mod.dict().values())
    res=Res_Modify()
    res.msg=msg
    res.data=data
    return res

@router.post('/put',response_model=Res)
async def put(id:int = Body(...,embed=True),
              content:str = Body(...,embed=True)) :
    msg=adminService.put(id,content)
    res=Res()
    res.msg=msg
    return res

@router.post('/finish',response_model=Res_Finish)
async def finish(fin:Finish) :
    msg,data=adminService.finish(*fin.dict().values())
    res=Res_Finish()
    res.msg=msg
    res.data=data
    return res

@router.post('/query',response_model=Res_Modify)
async def query(菜品id:int = Body(...,embed=True)) :
    msg,data=adminService.query(菜品id)
    res=Res_Modify()
    res.msg=msg
    res.data=data
    return res

@router.get('/show',response_model=Res_Show)
async def show() :
    msg,data=adminService.show()
    res=Res_Show()
    res.msg=msg
    res.data=data
    return res

@router.post('/delete',response_model=Res)
async def delete(id:int = Body(...,embed=True),
                 菜品id:int = Body(...,embed=True)) :
    msg=adminService.delete(id, 菜品id)
    res=Res()
    res.msg=msg
    return res

@router.post('/add',response_model=Res_Finish)
async def add(am:Add_Menu) :
    res=Res_Finish(msg=False)
    if adminService.check_empty(am.dict().values()) : 
        msg,data=adminService.add(*am.dict().values())
        res.data=data
        res.msg=msg
    return res   

@router.post('/upload_pic',response_model=Res)
async def upload_pic(file:UploadFile = File(...)) :
    try :
        with open('./pic/'+file.filename,"wb") as f :
            f.write(await file.read())
        msg="http://192.168.1.104:8000/static/"+file.filename
    except Exception :
        msg=""
    res=Res()
    res.msg=msg
    return res

@router.post('/create_user',response_model=Res_Finish)
async def create_user(cr:Create_User) :
    msg,data=adminService.create_user(*cr.dict().values())
    res=Res_Finish()
    res.msg=msg
    res.data=data
    return res

@router.post('/delete_user',response_model=Res)
async def delete_user(管理员id:int = Body(...,embed=True),
                      被删除id:int = Body(...,embed=True)) :
    msg=adminService.delete_user(管理员id, 被删除id)
    res=Res()
    res.msg=msg
    return res

@router.get('/show_user',response_model=Res_Show)
async def show_user() :
    msg,data=adminService.show_user()
    res=Res_Show()
    res.msg=msg
    res.data=data
    return res

@router.get('/query_menu',response_model=Res_Show)
async def query_menu() :
    msg,data=adminService.query_menu()
    res=Res_Show()
    res.msg=msg
    res.data=data
    return res

@router.post('/logout',response_model=Res)
async def logout(id:int = Body(...,embed=True)) :
    msg=adminService.logout(id)
    res=Res()
    res.msg=msg
    return res