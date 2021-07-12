# -*- coding: utf-8 -*-

from orderSystem.dao.serverDao import s
from datetime import datetime

def place_order(table:int,id:int,num:int,order:dict) :
    try :
        ans,dish_id=s.place_order(table, num, id, order)
        data={"订单编号":dish_id,"下单时间":datetime.now(),"菜品列表":order}
    except Exception :
        return 
    return ans,data

def window() :
    try :
        ans,data=s.window()
    except Exception :
        return 
    return ans,data

def broadcast() :
    try :
        ans,data=s.broadcast()
    except Exception :
        return 
    return ans,data

def show() :
    try :
        ans,data=s.show()
        cnt=0
        for item in data :
            for dish in item["订单内容"] :
                cnt+=int(dish["数量"])
            item.update({"菜品总数":cnt})
    except Exception :
        return False,[]
    return ans,data

def buy(table:int,id:int) :
    try :
        ans=s.buy(table, id)
    except Exception :
        return False 
    return ans

def logout(id:int) :
    try :
        ans=s.logout(id)
    except Exception :
        return False
    return ans

def pass_order() :
    try :
        ans,data=s.PASS()
    except Exception :
        return 
    return ans,data

def query_menu() :
    try :
        menu=s.query_menu()
        data=[]
        for i in menu :
            data.append({
                '菜品id':i[0],
                '菜品名称':i[1],
                '菜品价格':i[2],
                '图片':i[3],
                '简介':i[4],
                '是否推荐':i[5]
                }),
        msg=True
    except Exception :
        msg=False
        data=[]
        print("ERR query menu")
    return msg,data