# -*- coding: utf-8 -*-

from orderSystem.dao.serverDao import s
from datetime import datetime

def place_order(table:int,id:int,num:int,order:dict) :
    try :
        if s.query_job(id)!=1 :
            return False,{}
        if not s.query_login(id) :
            return False,{}
        ans,dish_id=s.place_order(table, num, id, order)
        data={"订单编号":dish_id,"下单时间":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"菜品列表":order}
    except Exception :
        return 
    return ans,data

def window() :
    try :
        ans,data=s.window()
    except Exception :
        return 
    return ans,data

def broadcast(id:int) :
    try :
        if s.query_job(id)!=1 :
            return False,{}
        if not s.query_login(id) :
            return False,{}
        ans,data=s.broadcast()
    except Exception :
        return 
    return ans,data

def show(id:int) :
    try :
        if s.query_job(id)!=1 :
            return False,{}
        if not s.query_login(id) :
            return False,{}
        ans,data=s.show()
        for item in data :
            cnt=0
            for dish in item["订单内容"] :
                cnt+=int(dish["数量"])
            item.update({"菜品总数":cnt})
    except Exception :
        return False,[]
    return ans,data

def buy(table:int,id:int) :
    try :
        if s.query_job(id)!=1 :
            return False,{}
        if not s.query_login(id) :
            return False,{}
        ans=s.buy(table, id)
    except Exception :
        return False 
    return ans

def logout(id:int) :
    try :
        if s.query_job(id)!=1 :
            return False,{}
        if not s.query_login(id) :
            return False,{}
        ans=s.logout(id)
    except Exception :
        return False
    return ans

def pass_order(id:int) :
    try :
        if s.query_job(id)!=1 :
            return False,{}
        if not s.query_login(id) :
            return False,{}
        ans,data=s.PASS()
    except Exception :
        return 
    return ans,data

def query_menu(id:int) :
    try :
        if s.query_job(id)!=1 :
            return False,[]
        if not s.query_login(id) :
            return False,[]
        menu=s.query_menu()
        data=[]
        for i in menu :
            if i[5] :
                rec="特色菜"
            else :
                rec="传统菜"
            data.append({
                '菜品id':i[0],
                '菜品名称':i[1],
                '菜品价格':i[2],
                '图片':i[3],
                '简介':i[4],
                '是否推荐':rec
                }),
        msg=True
    except Exception :
        msg=False
        data=[]
        print("ERR query menu")
    return msg,data