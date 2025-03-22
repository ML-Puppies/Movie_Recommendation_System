from K22416C.FINAL.Connectors.Connector import Connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the MySQL database
connector = Connector()
connector.connect()  

# Load data from the database
movies = connector.queryDataset("SELECT * FROM movies;")
ratings = connector.queryDataset("SELECT * FROM ratings;")
user = connector.queryDataset("SELECT * FROM user;")


# 3.1.2. Description of Variables
# Checking basic information about the dataset
print(movies.info())
print(ratings.info())

# Display summary statistics for numerical columns
print(movies.describe())
print(ratings.describe())

# Display unique values count for categorical columns
categorical_columns_movies = movies.select_dtypes(include=['object']).columns
for col in categorical_columns_movies:
    print(f"{col}: {movies[col].nunique()} unique values")
categorical_columns_ratings = ratings.select_dtypes(include=['object']).columns
for col in categorical_columns_ratings:
    print(f"{col}: {ratings[col].nunique()} unique values")

# checking data types of each column
print("movies dtype: ", movies.dtypes)
print("ratings dtype:", ratings.dtypes)

# Checking for missing values
print("\nChecking for missing values in movies dataset:")
print(movies.isnull().sum())

print("\nChecking for missing values in ratings dataset:")
print(ratings.isnull().sum())

# Checking percentage of missing values
print("\nPercentage of missing values in movies dataset:")
print((movies.isnull().sum() / len(movies)) * 100)

print("\nPercentage of missing values in ratings dataset:")
# 3.2.2. Converting data types
movies['movieId'] = pd.to_numeric(movies['movieId'], errors='coerce')
ratings['userId'] = pd.to_numeric(ratings['userId'], errors='coerce')
ratings['movieId'] = pd.to_numeric(ratings['movieId'], errors='coerce')
ratings['rating'] = pd.to_numeric(ratings['rating'], errors='coerce')

# Checking data types
print(movies.dtypes)
print(ratings.dtypes)

 # 3.2.3. Data Normalization
 # 1. Convert timestamp to datetime
ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')

# 2. Extract useful time-related features
ratings['year'] = ratings['timestamp'].dt.year
ratings['month'] = ratings['timestamp'].dt.month
ratings['day_of_week'] = ratings['timestamp'].dt.dayofweek
ratings['hour'] = ratings['timestamp'].dt.hour

# 3. Calculate elapsed time (years since the last rating)
latest_timestamp = ratings['year'].max()
ratings['elapsed_time'] = latest_timestamp - ratings['year']

# 4. Drop original timestamp column
ratings.drop(columns=['timestamp'], inplace=True)
print(ratings)

# 3.4.2. Create a 'release_year' column extracted from the 'title' in the movies dataset
movies['release_year'] = movies['title'].str.extract(r'\((\d{4})\)')

# 3.4.3 Convert the 'genres' column into a list
# Convert the 'genres' column into a list
# Change settings to display all column
pd.set_option('display.max_columns', None)
movies['genres'] = movies['genres'].apply(lambda x: x.split('|'))
# Display result
print(movies)
