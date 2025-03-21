from K22416C.FINAL.Connectors.Connector import Connector
from K22416C.FINAL.Connectors.Movie import Movie

class MovieConnector(Connector):
    def GetMoviesbyGenre(self,inputgenre):
        """Get a list of movies by genre"""
        cursor = self.conn.cursor()
        sql = """SELECT m.movieId, 
                 SUBSTRING_INDEX(m.title, ' (', 1) AS movie_name,  
                 SUBSTRING_INDEX(SUBSTRING_INDEX(m.title, '(', -1), ')', 1) AS release_year,  
                 m.genres, 
                 COALESCE(AVG(r.rating), 0) AS average_rating
                 FROM movies m
                 LEFT JOIN ratings r ON m.movieId = r.movieId
                 WHERE m.genres LIKE %s
                 GROUP BY m.movieId, movie_name, release_year, m.genres;"""
        val=('%' + inputgenre + '%',)
        cursor.execute(sql,val)
        dataset = cursor.fetchall()
        movieslistbygenre = []
        for item in dataset:
            movieslistbygenre.append(Movie(item[0],item[1],item[2],item[3],item[4]))
        cursor.close()
        return movieslistbygenre

    def GetDetail(self,movieId):
        """Get detailed information of a movie based on movieId"""
        cursor = self.conn.cursor()
        sql = """SELECT m.movieId, 
                 SUBSTRING_INDEX(m.title, ' (', 1) AS movie_name, 
                 SUBSTRING_INDEX(SUBSTRING_INDEX(m.title, '(', -1), ')', 1) AS release_year,  
                 m.genres, 
                 COALESCE(AVG(r.rating), 0) AS average_rating 
                 FROM movies m
                 JOIN ratings r ON m.movieId = r.movieId
                 WHERE m.movieId = %s  -- Filter by movieId
                 GROUP BY m.movieId, movie_name, release_year, m.genres;"""
        val=(movieId,)
        cursor.execute(sql, val)
        dataset = cursor.fetchone()
        movie=None
        if dataset is not None:
            movieId, title, release_year, genres, average_rating = dataset
            movie = Movie(movieId, title, release_year, genres, average_rating)
        cursor.close()
        return movie
