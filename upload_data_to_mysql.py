import pandas as pd
from sqlalchemy import create_engine

# Thông tin kết nối đến MySQL
user = "root"
password = "Giang0409$"
host = "localhost"  # Hoặc IP của MySQL Server
database = "movie_ratings"

# Tạo kết nối đến MySQL
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# Đọc 2 dataset từ file CSV
df1 = pd.read_csv("D:/TÀI LIỆU HỌC KỲ 8/Machine learning/Source Code/PycharmProjects/FinalProject/Dataset/movies.csv")  # Thay bằng tên file thực tế
df2 = pd.read_csv("D:/TÀI LIỆU HỌC KỲ 8/Machine learning/Source Code/PycharmProjects/FinalProject/Dataset/ratings.csv")
df3 = pd.read_csv("D:/TÀI LIỆU HỌC KỲ 8/Machine learning/Source Code/PycharmProjects/FinalProject/Dataset/user_account.csv")

# Đẩy dataset1 lên MySQL thành bảng 'table1'
df1.to_sql(name="movies", con=engine, if_exists="replace", index=False, chunksize=10000)

# Đẩy dataset2 lên MySQL thành bảng 'table2'
df2.to_sql(name="ratings", con=engine, if_exists="replace", index=False, chunksize=10000)

# Đẩy dataset3 lên MySQL thành bảng 'table3'
df3.to_sql(name="users", con=engine, if_exists="replace", index=False, chunksize=10000)

print("✅ Đã đẩy dữ liệu lên MySQL thành công!")
