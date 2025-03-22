import mysql.connector
import traceback
import pandas as pd

class Connector:
    def __init__(self, server="localhost", port=3306, database="movie_ratings", username="root", password="@Obama123"):
        self.server = server  # The server address (default is localhost)
        self.port = 3306  # Port number for MySQL (default is 3306)
        self.database = "movie_ratings"  # The name of the database
        self.username = "root"  # Username for MySQL login
        self.password = "@Obama123"  # Password for MySQL login
        self.conn = None  # This will hold the database connection

    def connect(self):
        """Establish a connection to the MySQL database"""
        try:
            # Attempt to connect to the MySQL database using the provided credentials
            self.conn = mysql.connector.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password)
            print("Database connection successful!")  # Connection success message
            return self.conn  # Return the connection object
        except Exception as e:
            # If an error occurs during connection, print the error and the stack trace
            print(f"Connection error: {e}")
            traceback.print_exc()
        return None  # Return None if the connection fails

    def disConnect(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()  # Close the connection
            print("Database connection closed.")  # Connection closed message

    def queryDataset(self, sql):
        """Execute an SQL query and return the result as a DataFrame"""
        try:
            cursor = self.conn.cursor()  # Create a cursor object to interact with the database
            cursor.execute(sql)  # Execute the SQL query
            df = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)  # Fetch all results and store in a DataFrame
            return df  # Return the DataFrame containing the query results
        except Exception as e:
            # If an error occurs during the query execution, print the error and the stack trace
            print(f"Query error: {e}")
            traceback.print_exc()
        return None  # Return None if the query fails

    def getTablesName(self):
        """Fetch and return the names of all tables in the database"""
        cursor = self.conn.cursor()  # Create a cursor object
        cursor.execute("SHOW TABLES;")  # Execute the command to show all tables
        results = cursor.fetchall()  # Fetch the result of the command
        return [item[0] for item in results]  # Return a list of table names
