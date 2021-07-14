import pymysql
from orderSystem.host_addr import *

from datetime import datetime

# 打开数据库连接

class cook():
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

    def show(self):
        """
        展示所有处于未烹饪和正在烹饪的订单
        0表示未烹饪，1表示正在烹饪，2表示完成烹饪
        完成烹饪的订单不会显示
        return: 处于未烹饪和正在烹饪状态的所有订单
        """
        data = list()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM DISH ORDER BY CREATE_TIME ASC;"
                cursor.execute(sql)
                results = cursor.fetchall()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        else:
            for i in range(len(results)):
                if (results[i][8] != 2):
                    data.append(
                        {'桌号': results[i][1], '菜名': results[i][5], '数量': results[i][6], '状态': str(results[i][8])})
        finally:
            self.conn.close()
        return ans, data

    def confirm(self, TABLE_NUMBER: int, DISH_NAME: str, DISH_NUMBER: int):
        """
        将输入订单的状态从未烹饪变成正在烹饪
        :param TABLE_NUMBER: 桌号
        :param DISH_NAME:菜名
        :param DISH_NUMBER:数量
        :return:True or False
        """
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "select create_time from DISH where table_number=%d AND dish_name='%s' AND dish_number=%d AND STATE=0 order by create_time asc;"
                cursor.execute(sql % (TABLE_NUMBER, DISH_NAME, DISH_NUMBER))
                t = cursor.fetchone()[0]
                print(t)
                sql = "UPDATE DISH SET STATE = 1 WHERE CREATE_TIME='%s' AND TABLE_NUMBER = '%d' AND DISH_NAME = '%s' AND DISH_NUMBER = '%d' AND STATE=0;"
                cursor.execute(sql % (t,TABLE_NUMBER, DISH_NAME, DISH_NUMBER))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans

    def finish(self, TABLE_NUMBER: int, DISH_NAME: str, DISH_NUMBER: int):
        """
        将输入订单的状态从正在烹饪变成完成烹饪
        :param TABLE_NUMBER: 桌号
        :param DISH_NAME:菜名
        :param DISH_NUMBER:数量
        :return:True or False
        """
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "select create_time from DISH where table_number=%d AND dish_name='%s' AND dish_number=%d AND STATE=1 order by create_time asc;"
                cursor.execute(sql % (TABLE_NUMBER, DISH_NAME, DISH_NUMBER))
                t = cursor.fetchone()[0]
                sql = "UPDATE DISH SET STATE = 2,CREATE_TIME='%s' WHERE CREATE_TIME='%s' AND TABLE_NUMBER = '%d' AND DISH_NAME = '%s' AND DISH_NUMBER = '%d' AND STATE=1;"
                cursor.execute(sql % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),t,
                                      TABLE_NUMBER, DISH_NAME, DISH_NUMBER))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        finally:
            self.conn.close()
        return ans

    def window(self):
        """
        状态为0表示未发布，状态为1表示已发布
        未发布的公告作为返回值返回后状态变为1
        :return: 返回值为True表示有未发布的公告,msg为该未发布的公告,返回值为False表示当前无未发布的公告
        """
        msg = list()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM NOTICE WHERE STATE = 0 order by create_time desc;"
                cursor.execute(sql)
                results = cursor.fetchone()
                sql = 'UPDATE NOTICE SET STATE = 1 WHERE NOTICE = "%s";'
                cursor.execute(sql % (results[0]))
            self.conn.commit()
            ans = True
        except Exception:
            self.conn.rollback()
            ans = False
        else:
            msg.append({'标题': results[2],'时间': results[1],'内容': results[0]})
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
                sql = "SELECT * FROM NOTICE ORDER BY CREATE_TIME DESC;"
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
    
try :
    c = cook()
except Exception :
    print("Fail to connect batabase.")