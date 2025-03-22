from Connectors.Connector import Connector
from Models.Preprocess import Preprocessing

connector = Connector()  # Kết nối cơ sở dữ liệu
connector.connect()  # Kết nối đến cơ sở dữ liệu
preprocessing = Preprocessing(connector)  # Khởi tạo đối tượng Preprocessing

# Tải và xử lý dữ liệu
preprocessing.load_data()  # Tải dữ liệu từ cơ sở dữ liệu
preprocessing.process()  # Xử lý dữ liệu

# Lấy các DataFrame đã xử lý
movies_df, ratings_df = preprocessing.get_dataframes()

# In ra các DataFrame
print("Movies DataFrame:")
print(movies_df.head())  # Hiển thị 5 dòng đầu của DataFrame movies

print("\nRatings DataFrame:")
print(ratings_df.head())  # Hiển thị 5 dòng đầu của DataFrame ratings

print("\nThông tin cơ bản của bảng 'movies':")
print(movies_df.info())
print("\nThông tin cơ bản của bảng 'ratings':")
print(ratings_df.info())

# Kiểm tra các giá trị thiếu (missing values)
print("\nSố lượng giá trị thiếu trong bảng 'movies':")
print(movies_df.isnull().sum())
print("\nSố lượng giá trị thiếu trong bảng 'ratings':")
print(ratings_df.isnull().sum())

# Kiểm tra sự trùng lặp giữa movieId trong bảng 'movies' và bảng 'ratings'
movie_ids_in_ratings = set(ratings_df['movieId'])
movie_ids_in_movies = set(movies_df['movieId'])
missing_in_movies = movie_ids_in_ratings - movie_ids_in_movies
missing_in_ratings = movie_ids_in_movies - movie_ids_in_ratings

print(f"\nSố lượng movieId trong 'ratings' không tồn tại trong 'movies': {len(missing_in_movies)}")
print(f"Số lượng movieId trong 'movies' không tồn tại trong 'ratings': {len(missing_in_ratings)}")

