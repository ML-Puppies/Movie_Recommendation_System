import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from K22416C.FINAL.Models.Preprocess import Preprocessing

class MoviesStatistic:
    def __init__(self, connector):
        """Khởi tạo lớp với dữ liệu từ Preprocessing."""
        self.connector = connector
        self.preprocessor = Preprocessing(self.connector)
        self.preprocessor.load_data()
        self.preprocessor.process()
        self.movies, self.ratings = self.preprocessor.get_dataframes()

    def top_10_movies_by_ratings(self, return_figure=False):
        """Top 10 most rated Movies"""
        ratings_count = self.ratings.groupby('movieId')['rating'].count().reset_index()
        top_movies_by_ratings_count = pd.merge(ratings_count, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_by_ratings_count = top_movies_by_ratings_count.sort_values(by='rating', ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(top_10_movies_by_ratings_count['title'], top_10_movies_by_ratings_count['rating'], color='darkred',
                edgecolor='black')
        ax.set_xlabel('Number of Ratings', fontsize=9, family='Arial')
        ax.set_title('Top 10 Most Rated Movies', fontsize=10, family='Arial')
        ax.invert_yaxis()
        plt.tight_layout()

        if return_figure:
            return fig  # Trả về Figure thay vì hiển thị
        else:
            plt.show()

    def top_genres_by_ratings(self, return_figure=False):
        """Hiển thị thể loại phim phổ biến theo số lượng đánh giá với Bubble Chart"""

        # Đưa cột 'genres' vào dạng phẳng (không phải list)
        all_genres = []
        for genres_list in self.movies['genres']:
            all_genres.extend(genres_list)

        genre_counts = Counter(all_genres)
        genre_counts_df = pd.DataFrame(genre_counts.items(), columns=['genre', 'num_movies'])

        # Nối dữ liệu ratings với movies
        genre_ratings = self.ratings.groupby('movieId')['rating'].count().reset_index()
        genre_ratings = pd.merge(genre_ratings, self.movies[['movieId', 'genres']], on='movieId', how='left')
        genre_ratings = genre_ratings.explode('genres')

        # Đếm số lượt đánh giá cho mỗi thể loại
        genre_ratings_count = genre_ratings.groupby('genres')['rating'].count().reset_index()
        genre_ratings_count.columns = ['genre', 'rating']

        # Kết hợp thông tin số lượng phim và số lượt đánh giá
        genre_summary = pd.merge(genre_counts_df, genre_ratings_count, on='genre', how='left')

        # Tạo Figure và Axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Vẽ biểu đồ Bubble Chart với tỷ lệ bóng rất nhỏ
        scatter = ax.scatter(
            genre_summary['genre'],
            genre_summary['rating'],
            s=genre_summary['num_movies'] * 3,  # Giảm tỷ lệ bóng xuống 0.5
            color='darkred', alpha=0.6, edgecolor='black'
        )

        # Ghi tên thể loại vào mỗi quả bóng
        for i, genre in enumerate(genre_summary['genre']):
            ax.text(genre_summary['genre'][i], genre_summary['rating'][i], genre, fontsize=9, ha='center', va='center')

        ax.set_xlabel('Genre')
        ax.set_ylabel('Number of Ratings')
        ax.set_title('Top Genres by Number of Ratings (Bubble Chart)', fontsize=12, family='Arial')

        # Xoay nhãn trục x để dễ đọc
        ax.set_xticklabels(genre_summary['genre'], rotation=45, ha='right')

        plt.tight_layout()

        if return_figure:
            return fig  # Trả về Figure để hiển thị trong PyQt hoặc nơi khác
        else:
            plt.show()  # Hiển thị nếu không cần trả về Figure

    def top_10_movies_with_5_stars(self, return_figure=False):
        """Hiển thị Top 10 phim có đánh giá 5 sao nhiều nhất"""
        # Lọc ra các đánh giá 5 sao
        five_star_ratings = self.ratings[self.ratings['rating'] == 5.0]
        five_star_count = five_star_ratings.groupby('movieId')['rating'].count().reset_index()
        top_movies_by_5_stars = pd.merge(five_star_count, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_by_5_stars = top_movies_by_5_stars.sort_values(by='rating', ascending=False).head(10)

        print(top_10_movies_by_5_stars[['title', 'rating']])  # Debugging output

        # Tạo Figure và Axes
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.barh(
            top_10_movies_by_5_stars['title'],
            top_10_movies_by_5_stars['rating'],
            color='darkred', edgecolor='black'
        )

        ax.set_xlabel('Number of 5-star Ratings')
        ax.set_title('Top 10 Movies with Most 5-Star Ratings')
        ax.invert_yaxis()  # Đảo ngược trục y để phim có nhiều đánh giá nhất nằm trên cùng

        plt.tight_layout()

        if return_figure:
            return fig  # Trả về Figure để hiển thị trong PyQt
        else:
            plt.show()  # Hiển thị nếu không cần trả về Figure

    def top_10_most_rated_movies_last_year(self, return_figure=False):
        """Finds and visualizes the top 10 most rated movies from the most recent year in the dataset."""

        # Đảm bảo cột 'release_year' là kiểu số
        self.movies['release_year'] = pd.to_numeric(self.movies['release_year'], errors='coerce')

        # Lấy năm phát hành mới nhất
        latest_year = self.movies['release_year'].max()

        # Lọc các bộ phim ra mắt trong năm này
        movies_last_year = self.movies[self.movies['release_year'] == latest_year]

        # Lọc các đánh giá của phim trong năm này
        ratings_last_year = self.ratings[self.ratings['movieId'].isin(movies_last_year['movieId'])]

        # Đảm bảo rằng cột 'rating' là kiểu số (float hoặc int)
        ratings_last_year['rating'] = pd.to_numeric(ratings_last_year['rating'], errors='coerce')

        # Loại bỏ các dòng có giá trị 'rating' không hợp lệ (NaN)
        ratings_last_year = ratings_last_year.dropna(subset=['rating'])

        # Đếm số lượt đánh giá cho mỗi phim
        ratings_count_last_year = ratings_last_year.groupby('movieId')['rating'].count().reset_index()

        # Ghép với tiêu đề phim
        top_movies_last_year = pd.merge(ratings_count_last_year, self.movies[['movieId', 'title']], on='movieId')

        # Sắp xếp và lấy top 10 phim
        top_10_movies_last_year = top_movies_last_year.sort_values(by='rating', ascending=False).head(10)

        print(top_10_movies_last_year[['title', 'rating']])  # Debugging output

        # Tạo Figure và Axes
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.barh(
            top_10_movies_last_year['title'],
            top_10_movies_last_year['rating'],
            color='darkred', edgecolor='black'
        )

        ax.set_xlabel('Number of Ratings')
        ax.set_title(f'Top 10 Most Rated Movies in {latest_year}')
        ax.invert_yaxis()  # Đảo ngược trục y để phim có nhiều đánh giá nhất nằm trên cùng

        plt.tight_layout()

        if return_figure:
            return fig  # Trả về Figure để hiển thị trong PyQt
        else:
            plt.show()  # Hiển thị nếu không cần trả về Figure

    def top_genres_over_time(self, return_figure=False):
        """Display the top 10 genres over time by the number of ratings."""
        genre_over_time = self.movies.explode('genres')
        genre_over_time = genre_over_time[genre_over_time['genres'] != '(no genres listed)']
        genre_count_by_year = genre_over_time.groupby(['release_year', 'genres']).size().reset_index(name='count')
        genre_counts = genre_count_by_year.groupby('genres')['count'].sum().reset_index()
        top_10_genres = genre_counts.nlargest(10, 'count')
        top_10_genre_data = genre_count_by_year[genre_count_by_year['genres'].isin(top_10_genres['genres'])]
        genre_pivot = top_10_genre_data.pivot(index='release_year', columns='genres', values='count').fillna(0)

        # Tạo Figure và Axes
        fig, ax = plt.subplots(figsize=(12, 8))

        genre_pivot.plot(kind='line', stacked=True, ax=ax)

        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Movies')
        ax.set_title('Top 10 Genres Over Time')
        ax.legend(title='Genres', bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()

        if return_figure:
            return fig  # Trả về Figure để hiển thị trong PyQt
        else:
            plt.show()  # Hiển thị nếu không cần trả về Figure

    def top_10_movies_by_most_rated_genre(self, return_figure=False):
        """Find the top 10 most rated movies in the most popular genre and return the plot as a Figure."""

        # Tách các thể loại và lọc bỏ mục không có thể loại
        genre_over_time = self.movies.explode('genres')
        genre_over_time = genre_over_time[genre_over_time['genres'] != '(no genres listed)']

        # Tìm thể loại phổ biến nhất
        genre_counts = genre_over_time['genres'].value_counts()
        most_popular_genre = genre_counts.idxmax()

        # Lọc các phim thuộc thể loại phổ biến nhất
        top_movies_by_genre = self.movies[self.movies['genres'].apply(lambda genres: most_popular_genre in genres)]

        # Đếm số lượt đánh giá cho các phim này
        ratings_count_by_genre = self.ratings[self.ratings['movieId'].isin(top_movies_by_genre['movieId'])]
        ratings_count_by_genre = ratings_count_by_genre.groupby('movieId')['rating'].count().reset_index()

        # Ghép với tiêu đề phim
        top_movies = pd.merge(ratings_count_by_genre, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_by_ratings = top_movies.sort_values(by='rating', ascending=False).head(10)

        # Tạo Figure và Axes
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(top_10_movies_by_ratings['title'], top_10_movies_by_ratings['rating'],
                color='darkred', edgecolor='black')
        ax.set_xlabel('Number of Ratings')
        ax.set_title(f'Top 10 Most Rated Movies in {most_popular_genre} Genre')
        ax.invert_yaxis()  # Đảo ngược trục y để phim có nhiều lượt đánh giá nhất nằm trên

        plt.tight_layout()

        if return_figure:
            return fig  # Trả về Figure nếu được yêu cầu
        else:
            plt.show()  # Hiển thị biểu đồ nếu không yêu cầu trả về

    def process(self):
        """Phương thức gọi tất cả các bước thống kê và vẽ biểu đồ cho phim"""
        self.top_10_movies_by_ratings()
        self.top_genres_by_ratings()
        self.top_10_movies_with_5_stars()
        self.top_10_most_rated_movies_last_year()
        self.top_genres_over_time()
        self.top_10_movies_by_most_rated_genre()



