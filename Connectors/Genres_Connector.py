from K22416C.FINAL.Connectors.Connector import Connector
from K22416C.FINAL.Connectors.Genres import Genres

class GenresConnector(Connector):
    def GetAllGenres(self):
    """ Retrieve a list of all unique movie genres"""
        cursor=self.conn.cursor()
        sql="""SELECT DISTINCT genre
               FROM movies, 
               JSON_TABLE(CONCAT('["', REPLACE(genres, '|', '","'), '"]'),
               '$[*]' COLUMNS (genre VARCHAR(50) PATH '$')) AS genre_table;"""
        cursor.execute(sql)
        dataset=cursor.fetchall()
        dsg=[]

        # Convert query results into a list of Genres objects
        for item in dataset:
            genres=item[0]
            dsg.append(Genres(genres))
        cursor.close()
        return dsg


