from K22416C.FINAL.Connectors.Connector import Connector

# MySQL connection information
server = "localhost"
port = 3306
database = "movie_ratings"
username = "root"
password = "@Obama123"

# Initialize the Connector object
db_connector = Connector(server, port, database, username, password)

# Connect to MySQL
connection = db_connector.connect()

if connection:
    print("Connection successful")

    # Try retrieving the list of tables
    tables = db_connector.getTablesName()
    print("List of tables:", tables)



