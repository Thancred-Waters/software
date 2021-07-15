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
        if id==-1:
            if not l.query_login(name) :
                job=-2
            msg = False
            pic = ""
        else :
            if job==0 and l.checkCook() :
                msg=False
            else :
                msg = l.login(id)
            pic = l.getPhoto(id) if msg else ""
    return msg,{'id':id,'name':name,'job':job,'pic':pic}