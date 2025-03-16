import pandas as pd

#CHAPTER 3: DATA PREPROCESSING AND ANALYSIS
# 3.2. Data preprocessing

class Preprocessing:
    def __init__(self, connector=None):
        self.connector = connector
        self.movies = None
        self.ratings = None

    def convert_data_types(self):
        """Converting dtype"""
        self.movies['movieId'] = pd.to_numeric(self.movies['movieId'], errors='coerce')
        self.ratings['userId'] = pd.to_numeric(self.ratings['userId'], errors='coerce')
        self.ratings['movieId'] = pd.to_numeric(self.ratings['movieId'], errors='coerce')
        self.ratings['rating'] = pd.to_numeric(self.ratings['rating'], errors='coerce')

    def extract_year_from_title(self):
        """Extract release year from 'title"""
        self.movies['release_year'] = self.movies['title'].str.extract(r'\((\d{4})\)')

    def timestamp_to_datetime(self):
        """Extract useful time-related features"""
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
        """missing value và loại bỏ các cột không cần thiết"""
        self.ratings.drop(columns=['timestamp'], inplace=True)

    def process(self):
        """Phương thức gọi tất cả các bước xử lý dữ liệu"""
        self.convert_data_types()
        self.extract_year_from_title()
        self.timestamp_to_datetime()
        self.calculate_elapsed_time()
        self.clean_data()


