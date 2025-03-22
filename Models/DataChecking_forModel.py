from Connectors.Connector import Connector
from Models.Preprocess import Preprocessing

connector = Connector()  # Connect to the database
connector.connect()  # Establish connection to the database
preprocessing = Preprocessing(connector)  # Initialize the Preprocessing object

# Load and process data by using Preprocess.py
preprocessing.load_data()  
preprocessing.process() 

# Retrieve the processed DataFrames
movies_df, ratings_df = preprocessing.get_dataframes()

# Print the DataFrames
print("Movies DataFrame:")
print(movies_df.head())  
print("\nRatings DataFrame:")
print(ratings_df.head())  

print("\nBasic information of the 'movies' table:")
print(movies_df.info())
print("\nBasic information of the 'ratings' table:")
print(ratings_df.info())

# Check for missing values
print("\nNumber of missing values in the 'movies' table:")
print(movies_df.isnull().sum())
print("\nNumber of missing values in the 'ratings' table:")
print(ratings_df.isnull().sum())

# Check for duplicates between movieId in the 'movies' and 'ratings' tables
movie_ids_in_ratings = set(ratings_df['movieId'])
movie_ids_in_movies = set(movies_df['movieId'])
missing_in_movies = movie_ids_in_ratings - movie_ids_in_movies
missing_in_ratings = movie_ids_in_movies - movie_ids_in_ratings

print(f"\nNumber of movieId in 'ratings' not found in 'movies': {len(missing_in_movies)}")
print(f"Number of movieId in 'movies' not found in 'ratings': {len(missing_in_ratings)}")
