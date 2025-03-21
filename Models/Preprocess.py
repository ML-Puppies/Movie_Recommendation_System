import pandas as pd

class Preprocessing:
    def __init__(self, connector):
        self.connector = connector
        self.movies = None

    def load_data(self):
        """Load dữ liệu từ MySQL"""
        self.movies = self.connector.queryDataset("SELECT * FROM movies;")
        self.ratings = self.connector.queryDataset("SELECT * FROM ratings;")

        # Kiểm tra dữ liệu bị None
        if self.movies is None:
            raise ValueError(
                "⚠ Lỗi: Không thể tải dữ liệu từ bảng 'movies'. Kiểm tra lại kết nối hoặc dữ liệu trong database!")

        if self.ratings is None:
            raise ValueError(
                "⚠ Lỗi: Không thể tải dữ liệu từ bảng 'ratings'. Kiểm tra lại kết nối hoặc dữ liệu trong database!")

        # Kiểm tra nếu DataFrame rỗng
        if self.movies.empty:
            raise ValueError("⚠ Lỗi: Bảng 'movies' không có dữ liệu!")

        if self.ratings.empty:
            raise ValueError("⚠ Lỗi: Bảng 'ratings' không có dữ liệu!")

        print("✅ Movies DataFrame:\n", self.movies.head())
        print("✅ Ratings DataFrame:\n", self.ratings.head())

    def convert_data_types(self):
        """Chuyển đổi kiểu dữ liệu"""
        self.movies['movieId'] = pd.to_numeric(self.movies['movieId'], errors='coerce')
        self.ratings['userId'] = pd.to_numeric(self.ratings['userId'], errors='coerce')
        self.ratings['movieId'] = pd.to_numeric(self.ratings['movieId'], errors='coerce')
        self.ratings['rating'] = pd.to_numeric(self.ratings['rating'], errors='coerce')

    def extract_year_from_title(self):
        """Trích xuất năm phát hành từ tiêu đề phim"""
        self.movies['release_year'] = self.movies['title'].str.extract(r'\((\d{4})\)')

    def timestamp_to_datetime(self):
        """Chuyển đổi timestamp thành datetime và trích xuất thông tin"""
        self.ratings['timestamp'] = pd.to_datetime(self.ratings['timestamp'], unit='s')
        self.ratings['year'] = self.ratings['timestamp'].dt.year
        self.ratings['month'] = self.ratings['timestamp'].dt.month
        self.ratings['day_of_week'] = self.ratings['timestamp'].dt.dayofweek
        self.ratings['hour'] = self.ratings['timestamp'].dt.hour

    def calculate_elapsed_time(self):
        """Tính khoảng thời gian từ năm hiện tại đến năm rating"""
        latest_timestamp = self.ratings['year'].max()
        self.ratings['elapsed_time'] = latest_timestamp - self.ratings['year']

    def clean_data(self):
        """Loại bỏ cột không cần thiết"""
        self.ratings.drop(columns=['timestamp'], inplace=True)

    def process(self):
        """Thực hiện tất cả các bước tiền xử lý"""
        print("🔍 Kiểm tra self.movies trước khi xử lý:", type(self.movies))
        print("🔍 Kiểm tra self.ratings trước khi xử lý:", type(self.ratings))

        if self.movies is None or self.ratings is None:
            raise ValueError("❌ Lỗi: self.movies hoặc self.ratings đã bị None trước khi xử lý!")

        self.convert_data_types()
        self.extract_year_from_title()
        self.timestamp_to_datetime()
        self.calculate_elapsed_time()
        self.clean_data()

    def get_dataframes(self):
        """Trả về hai DataFrame đã xử lý"""
        return self.movies, self.ratings