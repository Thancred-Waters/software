# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 15:15:05 2021

@author: zc
"""

import pymysql
from orderSystem.host_addr import *


# 打开数据库连接

class login():
    def reconnect(self):
        self.conn = pymysql.connect(
            host=url,
            user=user,
            password=password,
            # password="zctest",
            database=db,
            charset="utf8"
        )

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass
        
    def getList(self) :
        try :
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql="select * from employee where state=0;"
                cursor.execute(sql);
                res=cursor.fetchall()
            self.conn.commit()
            ans=True
        except Exception :
            self.conn.rollback()
            ans=False
            res=0
        finally :
            self.conn.close()
        return ans,res 
    
    def getPhoto(self,id:int) -> str:
        try :
            self.reconnect()
            with self.conn.cursor() as cursor :
                sql="select PHOTO from EMPLOYEE where ID=%d;"
                cursor.execute(sql % id)
                pic=cursor.fetchone()[0]
            self.conn.commit()
        except Exception :
            pic=""
            self.conn.rollback()
        finally :
            self.conn.close()
        return pic
                      
    def login(self,id:int):
        """
        根据传入的员工ID将其状态从0变成1
        :param id: 成功登录的员工的ID
        :return:
        """
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "UPDATE EMPLOYEE SET STATE = 1 WHERE ID =%d;"
                cursor.execute(sql % (id))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans
    
    def query_login(self,name:str) -> bool :
        """
        
        检验员工是否处于登录状态
        Parameters
        ----------
        id : int
            员工ID.

        Returns
        -------
        bool 
            True->员工已登录
            False->员工未登录.

        """
        try :
            self.reconnect()
            with self.conn.cursor() as cursor :
                sql="select STATE from EMPLOYEE WHERE PEOPLE_NAME='%s';"
                cursor.execute(sql % name);
                state=cursor.fetchone()[0]
            ans=True if state else False
            self.conn.commit()
        except Exception :
            ans=False
            self.conn.rollback()
        finally :
            self.conn.close()
        return ans       

l = login()


