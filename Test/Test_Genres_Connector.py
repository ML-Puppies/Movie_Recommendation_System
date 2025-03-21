from K22416C.FINAL.Connectors.Genres_Connector import GenresConnector

# Initialize the GenresConnector object and connect database
genresconn=GenresConnector()
genresconn.connect()

# Retrieve all movie genres
genreslist=genresconn.GetAllGenres()

print("Available movie genres: ")
for genres in genreslist:
    print(genres)