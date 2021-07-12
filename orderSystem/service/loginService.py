from orderSystem.dao.loginDao import l

def login(name:str,password:str) :
    """
    

    Parameters
    ----------
    name : str
        DESCRIPTION.
    password : str
        DESCRIPTION.

    Returns
    -------
    msg : TYPE
        DESCRIPTION.
    dict
        DESCRIPTION.

    """
    msg,user_list=l.getList()
    if msg:
        id = -1; job=-1
        for user in user_list :
            if user[1]==name and user[2]==password :
                id = user[0]; job=user[4]
                break
        if id==-1 :
            msg = False
        else :
            msg = l.login(id)
    return msg,{'id':id,'name':name,'job':job}