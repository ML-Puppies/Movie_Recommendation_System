class Movie:
    def __init__(self,movieId,title,release_year, genres,average_rating):
        self.movieId=movieId
        self.title=title
        self.release_year=release_year
        self.genres=genres
        self.average_rating=average_rating

    def __str__(self):
        msg=f"{self.movieId}\t{self.title}\t"\
            f"{self.release_year}\t{self.genres}\t"\
            f"{self.average_rating}"
        return msg

