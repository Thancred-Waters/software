# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 15:14:39 2021

@author: zc
"""

import time

import pymysql
from datetime import datetime
from orderSystem.host_addr import *


# 打开数据库连接

class Server():
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

    def place_order(self, TABLE_NUMBER: int, PEOPLE_NUMBER: int, EMPLOYEE: int, order: dict):
        """
        :param table: 桌号
        :param id: 下单服务员工号
        :param num: 下单人数
        :param order: 订单，包含菜品及数量
        :return:
        """
        try:
            self.reconnect()
            for i in order.keys():
                print(i)
                """
                i:DISH_NAME
                order[i]:DISH_NUMBER
                dish_price:PRICE
                """
                # 如果这个桌号对应的订单有
                dish_id = 0
                with self.conn.cursor() as cursor:
                    """
                    状态为0表示桌子未被占用,从当前id中选择最大的+1作为dish_id
                    状态为1表示桌子被占用,从当前id中选择桌号对应的id作为dish_id
                    
                    """
                    sql = 'SELECT TABLE_STATE FROM STATE WHERE TABLE_NUMBER= "%d";'
                    cursor.execute(sql % (TABLE_NUMBER))
                    state = cursor.fetchall()
                    if len(state) and (state[0][0] == 0):
                        
                        sql = "SELECT ID FROM DISH ORDER BY ID DESC;"
                        cursor.execute(sql)
                        id = cursor.fetchall()
                        # print(id)
                        dish_id = int(id[0][0]) + 1
                        # 改变桌子状态
                        sql = "UPDATE STATE SET TABLE_STATE = 1 WHERE TABLE_NUMBER = '%d';"
                        cursor.execute(sql % (TABLE_NUMBER))
                    else:
                        sql = "SELECT ID FROM DISH WHERE TABLE_NUMBER = '%d' ORDER BY ID DESC;"
                        cursor.execute(sql % (TABLE_NUMBER))
                        id = cursor.fetchall()
                        dish_id = int(id[0][0])
                    sql = 'SELECT PRICE FROM MENU WHERE DISH_NAME= "%s";'
                    cursor.execute(sql % (i))
                    dish_price = cursor.fetchall()
                    sql = "INSERT INTO DISH(ID,TABLE_NUMBER,PEOPLE,EMPLOYEE,CREATE_TIME,DISH_NAME,DISH_NUMBER,PRICE,STATE)" \
                          "VALUES (%d,%d,%d,%d,'%s','%s',%d,%f,%d);"
                    cursor.execute(sql % (dish_id, TABLE_NUMBER, PEOPLE_NUMBER, EMPLOYEE,
                                          datetime.now(),
                                          i, order[i], dish_price[0][0] * order[i], 0))
                self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans,dish_id

    def window(self):
        """
        状态为0表示未发布，状态为1表示已发布
        未发布的公告作为返回值返回后状态变为1
        :return: 返回值为True表示有未发布的公告,
        返回值为False表示当前无未发布的公告
        """
        msg = list()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM NOTICE WHERE STATE = 0 order by create_time DESC;"
                #将未发布的公告按照时间排序，发布最新公告
                cursor.execute(sql)
                results = cursor.fetchall()
                sql = 'UPDATE NOTICE SET STATE = 1 WHERE NOTICE = "%s";'
                if len(results) :
                    cursor.execute(sql % (results[0][0]))
                    msg.append({'标题': results[0][2], '时间': results[0][1].strftime("%Y-%m-%d %H:%M:%S"), '内容': results[0][0]})
                else :
                    raise Exception("No broadcast")
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False 
        finally:
            self.conn.close()
        return ans, msg


    def broadcast(self):
        """
        :return: 返回最近发布的公告
        """
        msg = list()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM NOTICE ORDER BY CREATE_TIME DESC"
                cursor.execute(sql)
                results = cursor.fetchall()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        else:
            for i in range(min(5,len(results))):
                msg.append({'标题': results[i][2],'时间': results[i][1],'内容': results[i][0]})
        finally:
            self.conn.close()
        return ans, msg

    def show(self):
        """
        展示所有订单
        :return: 所有订单
        """
        data = list()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM STATE WHERE TABLE_STATE!=0;"
                cursor.execute(sql)
                state = cursor.fetchall()
                #print(state)
                for i in range(len(state)):
                    #此处使用try-except捕获异常，保证抓取所有数据
                    try :
                        table_number=state[i][0]
                        sql = "SELECT ID FROM DISH WHERE TABLE_NUMBER=%d ORDER BY ID DESC;"
                        cursor.execute(sql % int(table_number))
                        id = cursor.fetchall()[0][0]
                        #print(id,type(id))
                        sql = "SELECT * FROM DISH WHERE ID=%d order by create_time asc;"
                        cursor.execute(sql % int(id))
                        dish= cursor.fetchall()
                        #print(dish)
                        dish_order=[]
                        sum_price=0
                        #print("*********************************************")
                        for j in range(0,len(dish)):
                            dish_order.append({"菜品名称":dish[j][5],'数量':dish[j][6],'价格':float(dish[j][7])})
                            sum_price+=float(dish[j][7])
                        #print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
                        #print(dish_order)
                        state_inter={0:'未使用',1:'正在用餐',2:'等待支付'}
                        data.append({'桌号':dish[0][1],'下单时间':dish[0][4],
                                     '金额':sum_price,'人数':dish[0][2],
                                     '订单状态':state_inter[int(state[i][1])],
                                     '订单内容':dish_order})     
                        #print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
                        print(data)
                    except Exception :
                        print("warning: server show")
                ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()   
        return ans,data

    def buy(self,table_number:int,employee_id:int):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = 'UPDATE STATE SET TABLE_STATE = 2 WHERE TABLE_NUMBER = %d;'
                # print(results[0][0])
                cursor.execute(sql % (table_number))  
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False     
        finally:
            self.conn.close()
        return ans


    def logout(self,id:int):
        """
        1表示已登录，0表示未登录
        退出需要将id对应员工的状态从1变成0
        :param id:退出登录的员工id
        :return: 退出成功或退出失败
        """
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "select state from employee where ID = %d;"
                cursor.execute(sql % (id))
                user = cursor.fetchall()
                if len(user)==0 or user[0][0]!=1:
                    raise Exception("fail to logout")
                #检查用户是否处在登陆状态，只有登陆状态才允许退出
                sql = "UPDATE EMPLOYEE SET STATE = 0 WHERE ID = '%d';"
                cursor.execute(sql % (id))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans

    def PASS(self):
        """
        :return:传菜
        """
        data = list()
        msg = dict()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT TABLE_NUMBER FROM STATE WHERE TABLE_STATE=1;"
                cursor.execute(sql)
                state = cursor.fetchall()
                for i in range(len(state)):
                    table_number = state[i][0]
                    sql = "SELECT ID FROM DISH WHERE TABLE_NUMBER=%d ORDER BY ID DESC;"
                    cursor.execute(sql % int(table_number))
                    id = cursor.fetchall()[0][0]
                    sql = "SELECT * FROM DISH WHERE ID=%d AND STATE = 2;"
                    cursor.execute(sql % int(id))
                    finished_dish = cursor.fetchall()
                    for j in range(len(finished_dish)):
                        data.append(",".join([str(finished_dish[j][1]),str(finished_dish[j][5]),str(finished_dish[j][3])]))
                    for j in range(len(data)):
                        msg.update({str(j+1):data[j]})
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans,msg
    
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

s = Server()