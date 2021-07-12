# -*- coding: utf-8 -*-

from orderSystem.dao.adminDao import a

def modify(dish_id:int,
           dish_name:str,
           price:float,
           recommend:str,
           description:str, 
           image:str) :
    try :
        msg,data=a.modify(dish_id, dish_name, price, recommend, description, image)
    except Exception :
        print("ERR modify")
    return msg,data

def put(id:int,
        content:str) :
    try :
        msg=a.put(id,content)
    except Exception :
        print("ERR put")
    return msg

def finish(id:int,
    订单号:str,
    是否免单:str,
    结账金额:float) :
    try :
        msg,data=a.finish(id, 订单号, 是否免单, 结账金额)
    except Exception :
        print("ERR finish")
    return msg,data

def query(id:int) :
    try :
        msg,data=a.query(id)
    except Exception :
        print("ERR query")
    return msg,data
    

def show() :
    try :
        msg,data=a.show()
    except Exception :
        print("ERR show")
    return msg,data

def delete(id:int,
           菜品id:int) :
    try :
        msg,data=a.delete(id,菜品id)
    except Exception :
        print("ERR delete")
    return msg,data

def add(id:int,
        菜名:str,
        价格:float,
        是否推荐:str,
        简介:str,
        图片:str) :
    try :
        msg,data=a.add(id,菜名,价格,是否推荐,简介,图片)
    except Exception :
        print("ERR add")
    return msg,data

def create_user(管理员id:int,
                创建用户名:str,
                密码:str,
                确认密码:str,
                身份:str,
                图片:str) :
    try :
        if 密码!=确认密码 :
            return False,{}
        if 身份=="管理员" :
            job=2
        elif 身份=="点餐员" :
            job=1
        else :
            job=0
        msg,id=a.create_user(管理员id,创建用户名,密码,job,图片)
        print("okkkkkkkkkkkkk")
        if msg :
            data={"员工id":id,"用户名":创建用户名,"身份":身份}
        else :
            data={}
    except Exception :
        print("ERR create user")
    return msg,data

def delete_user(管理员id:int,
                被删除id:int) :
    try :
        msg=a.delete_user(管理员id, 被删除id)
    except Exception :
        print("ERR delete user")
    return msg

def show_user() :
    try :
        msg,data=a.show_user()
        for user in data :
            if user["身份"]==0 :
                user["身份"]="后厨"
            elif user["身份"]==1 :
                user["身份"]="服务员"
            else :
                user["身份"]="管理员"
    except Exception:
        print("ERR show user")
    return msg,data

def query_menu() :
    try :
        menu=a.query_menu()
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

def logout(id:int) :
    try :
        msg=a.logout(id)
    except Exception:
        msg=False
        print("ERR logout")
    return msg