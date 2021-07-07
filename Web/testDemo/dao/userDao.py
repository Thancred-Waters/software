import pymysql

# 打开数据库连接

class DataBase() :
    def reconnect(self) :
        host = "localhost"
        #host = "192.168.0.142"
        self.conn=pymysql.connect(
            host=host,
            user="root",
            #password="tsh08040313",
            password="zctest",
            database="test",
            charset="utf8"
            )
        
    def __del__(self) :
        try :
            self.conn.close()
        except Exception :
            pass

    def show(self):
        student = dict()
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM STU"
                cursor.execute(sql)
                results = cursor.fetchall()
            ans=True
        except Exception:
            self.conn.rollback()
            ans=False
        else :
            for i in range(len(results)):
                student.update({results[i][0]: [results[i][1], results[i][2]]})
        finally :
            self.conn.close()
        return ans,student

    def add(self,id: str, name: str, age: int):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                # 创建一条新的记录
                sql = "INSERT INTO STU(ID,NAME,AGE)VALUES ('%s','%s',%d);"
                cursor.execute(sql % (id, name, age))
            self.conn.commit()
            ans=True
        except Exception: 
            self.conn.rollback()
            ans=False
        finally :
            self.conn.close()
        return ans

    def delete(self,id: str):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM STU WHERE ID='%s';"
                cursor.execute(sql % (id))
            self.conn.commit()
            ans=True
        except Exception:
            self.conn.rollback()
            ans=False
        finally :
            self.conn.close()
        return ans

    def edit(self,id: str, name: str, age: int):
        try:
            self.reconnect()
            with self.conn.cursor() as cursor:
                sql = "UPDATE STU SET NAME = '%s', AGE = '%d' WHERE ID = '%s';"
                cursor.execute(sql % (name, age, id))
            self.conn.commit()
            ans=True
        except Exception:
            self.conn.rollback()
            ans=False
        finally :
            self.conn.close()
        return ans

db=DataBase()