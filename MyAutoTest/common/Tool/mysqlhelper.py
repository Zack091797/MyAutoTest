import pymysql


class MySqlHelper:

    def __init__(self, database_info):
        self._database_info = database_info
        self.conn = None
        self.cursor = None

    def connectDB(self):
        try:
            self.conn = pymysql.connect(host=self._database_info.get("host", "127.0.0.1"),
                                        port=self._database_info.get("port", "3306"),
                                        user=self._database_info.get("user", "root"),
                                        password=self._database_info.get("password", "root"),
                                        database=self._database_info.get("database", "mysql"),
                                        charset=self._database_info.get("charset", "utf8"),
                                        connect_timeout=10)
            self.cursor = self.conn.cursor()
        except Exception as err:
            print(f"连接MySQL数据库失败!!!->{err}")

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as err:
            self.conn.rollback()
            print(f"数据库事务执行失败!!!->{err}")

    def query_data(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def insert_data(self, sql):
        pass

    def delete_data(self, sql):
        pass

    def update_data(self, sql):
        pass

    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        else:
            pass



