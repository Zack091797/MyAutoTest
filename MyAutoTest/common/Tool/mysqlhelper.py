import pymysql


class MySqlHelper:

    def __init__(self):
        self.db = pymysql.connect()
        self.cursor = self.db.cursor()

    def connect(self):
        pass

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def select(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def close(self):
        self.cursor.close()
        self.db.close()


sqlHelper = MySqlHelper()


