from K22416C.FINAL.Connectors.User_Connector import UserConnector
from K22416C.FINAL.Models.CollaborativeFiltering import MovieCollaborativeFiltering
from K22416C.FINAL.UI.recommend import Ui_MainWindow
from PyQt6.QtWidgets import QTableWidgetItem

class recommendExt(Ui_MainWindow):
    def __init__(self, user_connector, user_id):
        super().__init__()
        self.userconn = user_connector  # Use the existing UserConnector passed during login
        self.current_user_id = user_id  

        self.cf_model = None  # Collaborative filtering model will be initialized here

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # Initialize the collaborative filtering model
        self.initialize_CF_model()

        # Display the movie recommendations when the UI is set up
        self.display_recommendations()

    def showWindow(self):
        self.MainWindow.show()

    def get_current_user_id(self):
        return self.current_user_id  

    def initialize_CF_model(self):
        """Initialize the collaborative filtering model"""
        user_id = self.get_current_user_id() 
        if user_id is not None:
            # Initialize the collaborative filtering model
            self.cf_model = MovieCollaborativeFiltering(connector=self.userconn, k=10, uuCF=True)
            self.cf_model.processTrain()  # Train the model with the data
        else:
            print("No valid user ID found. Please log in again.")

    def display_recommendations(self):
        """Display recommendations for the current user"""
        user_id = self.get_current_user_id()  # Get the current user's ID
        if self.cf_model is not None and user_id is not None:
            recommendations = self.cf_model.recommend(user_id)

            self.tableWidget.setRowCount(0)  # Clear previous rows

            for movie_id, rating in recommendations:
                movie_info = self.userconn.queryDataset(f"SELECT title, genres FROM movies WHERE movieId = {movie_id}")

                if movie_info is not None and not movie_info.empty:  
                    title, genres = movie_info.iloc[0]  
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position)

                    self.tableWidget.setItem(row_position, 0, QTableWidgetItem(title))
                    self.tableWidget.setItem(row_position, 1, QTableWidgetItem(genres))
                    self.tableWidget.setItem(row_position, 2, QTableWidgetItem(f"{rating:.2f}"))
                else:
                    print(f"Movie information not found for movieId: {movie_id}")  
        else:
            print("No movie recommendations available.")

