import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import Counter

class MoviesStatistic:
    def __init__(self, connector=None):
        """Initializes the class with the movies and ratings DataFrames."""
        self.connector = connector
        self.lasted_df=None

    def execMovies(self, tableName=None):
        if tableName == None:
            sql = "select * from movies"
        else:
            sql = "select * from %s" %tableName
        self.df = self.connector.queryDataset(sql)
        self.lasted_df = self.df
        return self.df
    def execRatings(self, tableName=None):
        if tableName == None:
            sql = "select * from ratings"
        else:
            sql = "select * from %s" %tableName
        self.df = self.connector.queryDataset(sql)
        self.lasted_df = self.df
        return self.df

    def top_10_movies_by_ratings(self):
        """Top 10 most rated Movies"""
        ratings_count = self.ratings.groupby('movieId')['rating'].count().reset_index()
        top_movies_by_ratings_count = pd.merge(ratings_count, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_by_ratings_count = top_movies_by_ratings_count.sort_values(by='rating', ascending=False).head(10)
        print(top_10_movies_by_ratings_count[['title', 'rating']])

        plt.figure(figsize=(8, 6))
        plt.barh(top_10_movies_by_ratings_count['title'], top_10_movies_by_ratings_count['rating'], color='darkred',
                 edgecolor='black')
        plt.xlabel('Number of Ratings', fontsize=9, family='Arial')
        plt.title('Top 10 Most Rated Movies', fontsize=10, family='Arial')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def top_genres_by_ratings(self):
        """Hiển thị thể loại phim phổ biến theo số lượng đánh giá với Bubble Chart"""
        # Đưa cột 'genres' vào dạng phẳng (không phải list)
        all_genres = []
        for genres_list in self.movies['genres']:
            all_genres.extend(genres_list)
        genre_counts = Counter(all_genres)
        genre_counts_df = pd.DataFrame(genre_counts.items(), columns=['genre', 'num_movies'])
        genre_ratings = self.movies.explode('genres').groupby('genres')['rating'].count().reset_index()
        genre_summary = pd.merge(genre_counts_df, genre_ratings, left_on='genre', right_on='genres', how='left')
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(genre_summary['genre'], genre_summary['rating'], s=genre_summary['num_movies'] * 10,
                              color='darkred', alpha=0.6, edgecolor='black')
        for i, genre in enumerate(genre_summary['genre']):
            plt.text(genre_summary['genre'][i], genre_summary['rating'][i], genre, fontsize=9, ha='center', va='center')
        plt.xlabel('Genre')
        plt.ylabel('Number of Ratings')
        plt.title('Top Genres by Number of Ratings (Bubble Chart)', fontsize=12, family='Arial')

        # Xoay nhãn trục x để dễ đọc
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def top_10_movies_with_5_stars(self):
        """Hiển thị Top 10 phim có đánh giá 5 sao nhiều nhất"""
        # Lọc ra các đánh giá 5 sao
        five_star_ratings = self.ratings[self.ratings['rating'] == 5.0]
        five_star_count = five_star_ratings.groupby('movieId')['rating'].count().reset_index()
        top_movies_by_5_stars = pd.merge(five_star_count, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_by_5_stars = top_movies_by_5_stars.sort_values(by='rating', ascending=False).head(10)
        print(top_10_movies_by_5_stars[['title', 'rating']])
        plt.figure(figsize=(8, 6))
        plt.barh(top_10_movies_by_5_stars['title'], top_10_movies_by_5_stars['rating'], color='darkred',
                 edgecolor='black')
        plt.xlabel('Number of 5-star Ratings')
        plt.title('Top 10 Movies with Most 5-Star Ratings')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    def top_10_most_rated_movies_last_year(self):
        """Finds and visualizes the top 10 most rated movies from the most recent year in the dataset."""
        latest_year = self.movies['release_year'].max()
        movies_last_year = self.movies[self.movies['release_year'] == latest_year]
        ratings_last_year = self.ratings[self.ratings['movieId'].isin(movies_last_year['movieId'])]
        ratings_count_last_year = ratings_last_year.groupby('movieId')['rating'].count().reset_index()
        top_movies_last_year = pd.merge(ratings_count_last_year, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_last_year = top_movies_last_year.sort_values(by='rating', ascending=False).head(10)
        print(top_10_movies_last_year[['title', 'rating']])
        plt.figure(figsize=(8, 6))
        plt.barh(top_10_movies_last_year['title'], top_10_movies_last_year['rating'], color='darkred',
                 edgecolor='black')
        plt.xlabel('Number of Ratings')
        plt.title(f'Top 10 Most Rated Movies in {latest_year}')
        plt.gca().invert_yaxis()  # Invert the y-axis to display the highest rated movies at the top
        plt.tight_layout()
        plt.show()

    def top_genres_over_time(self):
        """Display the top 10 genres over time by the number of ratings."""
        genre_over_time = self.movies.explode('genres')
        genre_over_time = genre_over_time[genre_over_time['genres'] != '(no genres listed)']
        genre_count_by_year = genre_over_time.groupby(['release_year', 'genres']).size().reset_index(name='count')
        genre_counts = genre_count_by_year.groupby('genres')['count'].sum().reset_index()
        top_10_genres = genre_counts.nlargest(10, 'count')
        top_10_genre_data = genre_count_by_year[genre_count_by_year['genres'].isin(top_10_genres['genres'])]
        genre_pivot = top_10_genre_data.pivot(index='release_year', columns='genres', values='count').fillna(0)
        plt.figure(figsize=(12, 8))
        genre_pivot.plot(kind='line', stacked=True, figsize=(12, 8))

        plt.xlabel('Year')
        plt.ylabel('Number of Movies')
        plt.title('Top 10 Genres Over Time')
        plt.legend(title='Genres', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    def top_10_movies_by_ratings_last_month(self):
        """Finds and visualizes the top 10 most rated movies from the last month in the dataset."""
        # Convert 'timestamp' to datetime if it's not already in that format
        if 'timestamp' in self.ratings.columns:
            self.ratings['timestamp'] = pd.to_datetime(self.ratings['timestamp'], unit='s')
        self.ratings['year_month'] = self.ratings['timestamp'].dt.to_period('M')
        latest_month = self.ratings['year_month'].max()
        ratings_last_month = self.ratings[self.ratings['year_month'] == latest_month]
        ratings_count_last_month = ratings_last_month.groupby('movieId')['rating'].count().reset_index()
        top_movies_last_month = pd.merge(ratings_count_last_month, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_last_month = top_movies_last_month.sort_values(by='rating', ascending=False).head(10)
        print(top_10_movies_last_month[['title', 'rating']])
        plt.figure(figsize=(8, 6))
        plt.barh(top_10_movies_last_month['title'], top_10_movies_last_month['rating'], color='darkred',
                 edgecolor='black')
        plt.xlabel('Number of Ratings')
        plt.title(f'Top 10 Most Rated Movies in {latest_month}')
        plt.gca().invert_yaxis()  # Invert the y-axis to display the highest rated movies at the top
        plt.tight_layout()
        plt.show()

    def top_10_movies_by_most_rated_genre(self):
        """Find the top 10 most rated movies in the most popular genre."""
        genre_over_time = self.movies.explode('genres')
        genre_over_time = genre_over_time[genre_over_time['genres'] != '(no genres listed)']
        genre_counts = genre_over_time['genres'].value_counts()
        most_popular_genre = genre_counts.idxmax()
        top_movies_by_genre = self.movies[self.movies['genres'].apply(lambda genres: most_popular_genre in genres)]
        ratings_count_by_genre = self.ratings[self.ratings['movieId'].isin(top_movies_by_genre['movieId'])]
        ratings_count_by_genre = ratings_count_by_genre.groupby('movieId')['rating'].count().reset_index()
        top_movies = pd.merge(ratings_count_by_genre, self.movies[['movieId', 'title']], on='movieId')
        top_10_movies_by_ratings = top_movies.sort_values(by='rating', ascending=False).head(10)
        print(top_10_movies_by_ratings[['title', 'rating']])
        plt.figure(figsize=(8, 6))
        plt.barh(top_10_movies_by_ratings['title'], top_10_movies_by_ratings['rating'], color='darkred',
                 edgecolor='black')
        plt.xlabel('Number of Ratings')
        plt.title(f'Top 10 Most Rated Movies in {most_popular_genre} Genre')
        plt.gca().invert_yaxis()  # Đảo ngược trục y để hiển thị các phim được đánh giá nhiều nhất ở trên cùng
        plt.tight_layout()
        plt.show()

    def process(self):
        """Phương thức gọi tất cả các bước thống kê và vẽ biểu đồ cho phim"""
        self.top_10_movies_by_ratings()
        self.top_genres_by_ratings()
        self.top_10_movies_with_5_stars()
        self.top_10_most_rated_movies_last_year()
        self.top_genres_over_time()
        self.top_10_movies_by_ratings_last_month()
        self.top_10_movies_by_most_rated_genre()



