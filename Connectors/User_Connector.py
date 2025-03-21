from K22416C.FINAL.Connectors.Connector import Connector
from K22416C.FINAL.Connectors.User import User


class UserConnector(Connector):
    def __init__(self):
        super().__init__()
        self.current_user_id = None # Stores the userId of the currently logged-in user for recommendation

    # Authenticates login credentials, returns a User object if valid, otherwise returns None
    def login(self, userId, password):
        cursor = self.conn.cursor()
        sql = "SELECT * FROM user WHERE userID = %s AND password = %s"
        val = (userId, password)
        cursor.execute(sql, val)
        dataset = cursor.fetchone()
        user = None

        if dataset is not None:
            userId, password = dataset
            user = User(userId, password)

        cursor.close()
        return user

