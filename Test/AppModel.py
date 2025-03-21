from K22416C.FINAL.Connectors.Connector import Connector
from K22416C.FINAL.Models.Preprocess import Preprocessing

# Kết nối database
connector = Connector()
connector.connect()

# Tạo đối tượng tiền xử lý
preprocessor = Preprocessing(connector)
preprocessor.load_data()
preprocessor.process()

# Lấy dữ liệu đã xử lý
df_movies, df_ratings = preprocessor.get_dataframes()

# Hiển thị thông tin kiểm tra
#print(df_movies.head())
#print(df_ratings.head())
#print(df_movies.dtypes)
#print(df_ratings.dtypes)

print("Unique movieId in df_movies:", df_movies['movieId'].nunique())
print("Unique movieId in df_ratings:", df_ratings['movieId'].nunique())
print("Common movieId count:", len(set(df_movies['movieId']) & set(df_ratings['movieId'])))

# Đóng kết nối
connector.disConnect()