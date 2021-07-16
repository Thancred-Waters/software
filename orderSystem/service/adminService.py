# -*- coding: utf-8 -*-

from orderSystem.dao.adminDao import a

def check_empty(token : list) -> bool :
    for i in token :
        if isinstance(i,str) and i=="" :
            return False
        if isinstance(i,int) and i==0 :
            return False
        if isinstance(i,float) and i==0.0 :
            return False
    return True

def broadcast(id:int) :
    try :
        if a.query_job(id)<2 :
            return False,{}
        if not a.query_login(id) :
            return False,{}
        ans,data=a.broadcast()
    except Exception :
        return False,{}
    return ans,data

def modify(id:int,
           dish_id:int,
           dish_name:str,
           price:float,
           recommend:str,
           description:str, 
           image:str) :
    try :
        if a.query_job(id)<2 :
            return False,{}
        if not a.query_login(id) :
            return False,{}
        if recommend=="特色菜" :
            recommend=1
        else :
            recommend=0
        msg,data=a.modify(dish_id, dish_name, price, recommend, description, image)
        if data["是否推荐"]=="1" :
            data["是否推荐"]="特色菜"
        else :
            data["是否推荐"]="传统菜"
    except Exception :
        print("ERR modify")
        return False,{}
    return msg,data

def put(id:int,
        content:str) :
    try :
        if a.query_job(id)<2 :
            return False
        if not a.query_login(id) :
            return False
        msg=a.put(id,content)
    except Exception :
        print("ERR put")
        return False
    return msg

def finish(id:int,
    订单号:str,
    是否免单:str,
    结账金额:float) :
    try :
        if a.query_job(id)<2 :
            return False,{}
        if not a.query_login(id) :
            return False,{}
        msg,data=a.finish(id, 订单号, 是否免单, 结账金额)
    except Exception :
        msg=False
        data={}
        print("ERR finish")
    return msg,data

def query(id:int,
          菜品id:int) :
    try :
        if a.query_job(id)<2 :
            return False,{}
        if not a.query_login(id) :
            return False,{}
        msg,data=a.query(菜品id)
        if data["是否推荐"] :
            data["是否推荐"]="特色菜"
        else :
            data["是否推荐"]="传统菜"
    except Exception :
        print("ERR query")
        return False,{}
    return msg,data

def show(id:int) :
    try :
        if a.query_job(id)<2 :
            return False,[]
        if not a.query_login(id) :
            return False,[]
        msg,data=a.show()
        for item in data :
            cnt=0
            for dish in item["订单内容"] :
                cnt+=int(dish["数量"])
            item.update({"菜品总数":cnt})
    except Exception :
        print("ERR show")
        return False,[]
    return msg,data

def delete(id:int,
           菜品id:int) :
    try :
        if a.query_job(id)<2 :
            return False
        if not a.query_login(id) :
            return False
        msg=a.delete(id,菜品id)
    except Exception :
        print("ERR delete")
        return False
    return msg

def add(id:int,
        菜名:str,
        价格:float,
        是否推荐:str,
        简介:str,
        图片:str) :
    try :
        if a.query_job(id)<2 :
            return False,{}
        if not a.query_login(id) :
            return False,{}
        if 是否推荐=="特色菜" :
            是否推荐=1
        else :
            是否推荐=0
        if not a.query_same_dish(菜名) :
            msg=False
            data={}
        else :
            msg,data=a.add(id,菜名,价格,是否推荐,简介,图片)
    except Exception :
        msg=False
        data={}
        print("ERR add")
    return msg,data

def create_user(管理员id:int,
                创建用户名:str,
                密码:str,
                确认密码:str,
                身份:str,
                图片:str) :
    try :
        admin_job:int = a.query_job(管理员id)
        if admin_job<2 :
            return False,{}
        if not a.query_login(管理员id) :
            return False,{}
        if 密码!=确认密码 :
            return False,{}
        if admin_job==2 and 身份=="管理员":
            return False,{}
        if not a.query_same_name(创建用户名) :
            return False,{}
        if 身份=="点餐员" :
            job=1
        elif 身份=="后厨" :
            job=0
        else :
            job=2
        msg,id=a.create_user(管理员id,创建用户名,密码,job,图片)
        if msg :
            data={"员工id":id,"用户名":创建用户名,"身份":身份}
        else :
            data={}
    except Exception :
        print("ERR create user")
        return False,{}
    return msg,data

def delete_user(管理员id:int,
                被删除id:int) :
    """
    

    Parameters
    ----------
    管理员id : int
        删除用户的管理员.
    被删除id : int
        被删除用户的id.

    Returns
    -------
    TYPE
        返回True/False表示是否删除成功.

    """
    try :
        admin_job:int = a.query_job(管理员id)
        user_job:int = a.query_job(被删除id)
        if admin_job<2 :
            return False
        if not a.query_login(管理员id) :
            return False
        if admin_job==2 and user_job>=2 :
            return False
        if admin_job==3 and user_job==3 :
            return False
        if user_job==-1 :
            return False
        msg=a.delete_user(管理员id, 被删除id)
    except Exception :
        print("ERR delete user")
        return False
    return msg

def show_user(id:int) :
    """
    对管理员展示所有用户的信息

    Returns
    -------
    msg : TYPE
        请求是否成功.
    data : TYPE
        用户数据.

    """
    try :
        if a.query_job(id)<2 :
            return False,[]
        if not a.query_login(id) :
            return False,[]
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
        return False,[]
    return msg,data

def modify_user(管理员id:int,
                员工id:int,
                用户名:str,
                密码:str,
                图片:str) :
    try :
        admin_job:int = a.query_job(管理员id)
        user_job:int = a.query_job(员工id)
        if admin_job<2 :
            return False
        if not a.query_login(管理员id) :
            return False
        if admin_job==2 and user_job>=2 :
            return False
        a.empty_name(用户名)
        if not a.query_same_name(用户名) :
            return False
        msg=a.modify_user(管理员id, 员工id, 用户名,密码, 图片)
    except Exception:
        msg=False
        print("ERR show user")
    return msg
    
def query_menu(id:int) :
    try :
        if a.query_job(id)<2 :
            return False,[]
        if not a.query_login(id) :
            return False,[]
        menu=a.query_menu()
        data=[]
        for i in menu :
            rec = i[5]
            if rec==1 :
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

def logout(id:int) :
    try :
        msg=a.logout(id)
    except Exception:
        msg=False
        print("ERR logout")
    return msg