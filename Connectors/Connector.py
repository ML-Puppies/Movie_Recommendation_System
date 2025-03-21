import mysql.connector
import traceback
import pandas as pd

class Connector:
    def __init__(self, server="localhost", port=3306, database="movie_ratings", username="root", password="@Obama123"):
        self.server = server
        self.port = 3306
        self.database = "movie_ratings"
        self.username = "root"
        self.password = "@Obama123"
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password)
            print("✅ Kết nối cơ sở dữ liệu thành công!")
            return self.conn
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            traceback.print_exc()
        return None

    def disConnect(self):
        if self.conn:
            self.conn.close()
            print("🔌 Đã ngắt kết nối cơ sở dữ liệu.")

    def queryDataset(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
            return df
        except Exception as e:
            print(f"❌ Lỗi truy vấn dữ liệu: {e}")
            traceback.print_exc()
        return None

    def getTablesName(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES;")
        results = cursor.fetchall()
        return [item[0] for item in results]
