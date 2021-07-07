from testDemo.dao.userDao import db

def showUser():
    return db.show()

def addUser(id:str,name:str,age:int) :
    return db.add(id,name,age)

def deleteUser(id:str) :
    return db.delete(id)

def editUser(id:str,name:str,age:int) :
    return db.edit(id,name,age)