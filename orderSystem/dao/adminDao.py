# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 15:14:54 2021

@author: zc
"""

import time

import pymysql
from orderSystem.host_addr import *


# 打开数据库连接

class admin():
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

    def modify(self, ID: int, DISH_NAME: str, PRICE: float, RECOM: str, INTRO: str, PHOTO: str):
        """
        保持ID不变，更新其他参数
        :return: 更新后的各项参数
        """
        
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = 'UPDATE MENU SET DISH_NAME="%s",PRICE=%f,RECOM=%d,INTRO="%s",PHOTO="%s" WHERE ID = %d;'
                cursor.execute(sql % (DISH_NAME, PRICE, int(RECOM), INTRO, PHOTO, ID))  
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans, {'菜品id': ID, '菜名': DISH_NAME, '价格': PRICE, '是否推荐': RECOM, '简介': INTRO, '图片': PHOTO}

    def put(self, id: int, content: str ):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT PEOPLE_NAME FROM EMPLOYEE WHERE ID =%d;"
                cursor.execute(sql % id)
                name = cursor.fetchall()[0][0]
                sql = 'INSERT INTO NOTICE(NOTICE, CREATE_TIME, NAME, STATE) VALUES("%s", "%s", "%s", 0);'
                cursor.execute(sql % (content, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), name))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans

    def finish(self, EMPLOYEE: int, TABLE_NUMBER: str, FREE: str, MONEY: float):
        """
        根据传来的桌号处理买单服务
        :return:
        """
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = 'UPDATE STATE SET TABLE_STATE=0 WHERE TABLE_NUMBER=%d;'
                cursor.execute(sql % (TABLE_NUMBER))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        if FREE == "1" :#当免单为1时，减免所有费用
            MONEY=0
        return ans, {'id': EMPLOYEE, '桌号': TABLE_NUMBER, '订单状态': '支付完成', '实际是否免单': FREE, '实际支付金额': MONEY}

    def query(self, id: int):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM MENU WHERE ID =%d;"
                cursor.execute(sql % id)
                data = cursor.fetchall()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()

        return ans, {'菜品id': data[0][0], '菜名': data[0][1], '价格': float(data[0][2]), '是否推荐': str(data[0][5]),
                     '简介': data[0][4], '图片': data[0][3]}

    def show(self):
        """
        展示所有订单
        :return: 所有订单
        """
        data = list()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM STATE WHERE TABLE_STATE!=0"
                cursor.execute(sql)
                state = cursor.fetchall()
                for i in range(len(state)):
                    table_number = state[i][0]
                    sql = "SELECT ID FROM DISH WHERE TABLE_NUMBER='%d' ORDER BY ID DESC"
                    cursor.execute(sql % table_number)
                    id = cursor.fetchall()[0][0]
                    sql = "SELECT * FROM DISH WHERE ID='%d' order by create_time asc"
                    cursor.execute(sql % id)
                    dish = cursor.fetchall()
                    dish_order = dict()
                    sum_price = 0
                    for j in range(len(dish)):
                        dish_order.update({dish[j][5]: {'数量': dish[j][6], '价格': float(dish[j][7])}})
                        sum_price += float(dish[j][7])
                    state_inter = {0: '未使用', 1: '正在用餐', 2: '等待支付'}
                    data.append({'桌号': dish[0][1], '下单时间': dish[0][4].strftime("%Y-%m-%d %H:%M:%S"), '金额': sum_price,
                                 '人数': dish[0][2], '订单状态': state_inter[state[i][1]], '订单内容': dish_order})
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans, data

    def delete(self, id: int, dish_id: int):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM MENU WHERE ID=%d;"
                cursor.execute(sql % (dish_id))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans

    def add(self, ID: int, DISH_NAME: str, PRICE: float, RECOM: str, INTRO: str, PHOTO: str):
        """
        :return: 更新后的各项参数
        """
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = 'INSERT INTO MENU (ID,DISH_NAME,PRICE,PHOTO,INTRO,RECOM) VALUES(%d,"%s",%f,"%s","%s",%d);'
                cursor.execute(sql % (ID, DISH_NAME, PRICE, PHOTO, INTRO, int(RECOM)))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans, {'菜品id': ID, '菜名': DISH_NAME, '价格': PRICE, '是否推荐': RECOM, '简介': INTRO, '图片': PHOTO}

    def create_user(self, admin_id: int, employee_name: str, password: str, job: int, photo:str):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                # 创建一条新的记录
                sql = "INSERT INTO EMPLOYEE (PEOPLE_NAME,LOGIN_PASSWORD,PHOTO,JOB,STATE) VALUES ('%s','%s','%s',%d,%d);"
                print(employee_name, password,photo,job,0)
                cursor.execute(sql % (employee_name,password,photo,job,0))
                sql = "select id from EMPLOYEE order by id desc;"
                cursor.execute(sql)
                res=cursor.fetchall()[0][0]
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans,res

    def delete_user(self, admin_id: int, id: int):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM EMPLOYEE WHERE ID=%d;"
                cursor.execute(sql % (id))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans

    def show_user(self):
        data=list()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM EMPLOYEE;"
                cursor.execute(sql)
                results = cursor.fetchall()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        else:
            for i in range(len(results)):
                data.append({'员工id':results[i][0],'用户名':results[i][1],
                             '图片':"http://"+results[i][3],'身份':results[i][4]})
        finally:
            self.conn.close()
        return ans,data
    
    def query_menu(self) :
        try :
            self.reconnect()
            with self.conn.cursor() as cursor :
                sql="select * from menu;"
                cursor.execute(sql)
                res=cursor.fetchall()
            self.conn.commit()
        except Exception :
            self.conn.rollback()
        finally:
            self.conn.close()
        return res
    
    def logout(self,id:int) :
        try :
            self.reconnect()
            with self.conn.cursor() as cursor :
                sql="select state from employee where id=%d;"
                cursor.execute(sql % id)
                res=cursor.fetchall()
                if len(res)==0 or res[0][0]!=1 :
                    raise Exception("Fail to logout")
                sql="update employee set state=0 where id=%d;"
                cursor.execute(sql % id)
            self.conn.commit()
            msg=True
        except Exception:
            msg=False
            self.conn.rollback()
        finally :
            self.conn.close()
        return msg
        
a = admin()