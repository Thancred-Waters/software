from orderSystem.dao.cookDao import c

def show() :
    """
    返回菜品列表
    """
    try:
        ans,data=c.show()
    except Exception :
        pass
    return ans,data

def confirm(table:int,name:str,num:int) :
    """
    返回后厨是否成功确认菜品
    """
    try:
        ans=c.confirm(table,name,num)
    except Exception :
        pass
    return ans

def finish(table:int,name:str,num:int) :
    """
    返回后厨是否成功结束菜品
    """
    try:
        ans=c.finish(table,name,num)
    except Exception :
        pass
    return ans

def window() :
    """
    返回后厨是否收到弹窗信息，
    如果收到，同时返回最新公告
    """
    try:
        ans,data=c.window()
    except Exception :
        pass
    return ans,data

def broadcast() :
    """
    返回后厨是否收到历史公告信息，
    如果收到，同时返回公告
    """
    try:
        ans,data=c.broadcast()
    except Exception :
        pass
    return ans,data

def logout(id:int) :
    """
    

    Parameters
    ----------
    id : int
        登出者id.

    Returns
    -------
    ans : TYPE
        返回后厨是否成功登出.

    """
    try :
        ans=c.logout(id)
    except Exception :
        pass
    return ans