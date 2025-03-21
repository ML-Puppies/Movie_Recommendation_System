from K22416C.FINAL.Connectors.Movie_Connector import MovieConnector

# Initialize the MovieConnector object and connect database
movieconn=MovieConnector()
movieconn.connect()

# Retrieve the list of movies in the "Comedy" genre
movieslistbygenre=movieconn.GetMoviesbyGenre("Comedy")
print("List of movies in the Comedy genre: ")
for p in movieslistbygenre:
    print(p)

# Retrieve movie details for the movie with ID = 1
movieId=1
movieconn.connect()
movie=movieconn.GetDetail(movieId)

if movie!=None:
    print("*"*20)
    print("Movie with ID = 1: ")
    print(movie)