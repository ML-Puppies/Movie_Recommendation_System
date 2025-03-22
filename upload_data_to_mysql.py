import pandas as pd
from sqlalchemy import create_engine

# MySQL connection details
user = "root"
password = "Giang0409$"
host = "localhost" 
database = "movie_ratings"

# Create a connection to the MySQL database
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# Read datasets from CSV files
df1 = pd.read_csv("D:/TÀI LIỆU HỌC KỲ 8/Machine learning/Source Code/PycharmProjects/FinalProject/Dataset/movies.csv")  
df2 = pd.read_csv("D:/TÀI LIỆU HỌC KỲ 8/Machine learning/Source Code/PycharmProjects/FinalProject/Dataset/ratings.csv")
df3 = pd.read_csv("D:/TÀI LIỆU HỌC KỲ 8/Machine learning/Source Code/PycharmProjects/FinalProject/Dataset/user_account.csv")

# Upload dataset1 to MySQL as the 'movies' table
df1.to_sql(name="movies", con=engine, if_exists="replace", index=False, chunksize=10000)

# Upload dataset2 to MySQL as the 'ratings' table
df2.to_sql(name="ratings", con=engine, if_exists="replace", index=False, chunksize=10000)

# Upload dataset3 to MySQL as the 'users' table
df3.to_sql(name="users", con=engine, if_exists="replace", index=False, chunksize=10000)

print("Data has been successfully uploaded to MySQL!")
