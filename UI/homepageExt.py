import traceback

from PyQt6.QtWidgets import QListWidgetItem, QTableWidgetItem, QMainWindow
from PyQt6.QtCore import Qt
from K22416C.FINAL.Connectors.Connector import Connector

from K22416C.FINAL.Connectors.Genres_Connector import GenresConnector
from K22416C.FINAL.Connectors.Movie_Connector import MovieConnector
from K22416C.FINAL.UI.homepage import Ui_MainWindow

from K22416C.FINAL.UI.recommendExt import recommendExt
from K22416C.FINAL.UI.statisticExt import statisticExt

class homepageExt(Ui_MainWindow):
    def __init__(self,user_connector, user_id):
        self.userconn = user_connector
        self.current_user_id = user_id # Store current user ID for recommendation
        print(f"Current user ID in homepageExt: {self.current_user_id}")
        self.connector = Connector()  # Thêm dòng này để tạo đối tượng connector

        self.genresconn = GenresConnector()
        self.genreslist = []
        self.movieconn = MovieConnector()
        self.movieslist = []
        self.current_selected_genre = None


    def get_current_user_id(self):
        return self.current_user_id

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.query_genreslist()
        self.show_genreslist()
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def show_genreslist(self):
        self.listWidget_genresList.clear()
        for genre in self.genreslist:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, genre)
            item.setText(genre.genres)
            self.listWidget_genresList.addItem(item)

    def query_genreslist(self):
        self.genresconn.connect()
        self.genreslist = self.genresconn.GetAllGenres()

    def setupSignalAndSlot(self):
        self.listWidget_genresList.itemSelectionChanged.connect(self.show_moviestable)
        self.tableWidget_moviesList.itemSelectionChanged.connect(self.show_movie_details)
        self.pushButton_Recommend.clicked.connect(self.switch_recommend_window)
        self.pushButton_Statistic.clicked.connect(self.switch_statistic_window)

    def show_moviestable(self):
        try:
            selected_index = self.listWidget_genresList.currentRow()
            if selected_index < 0:
                return
            item = self.listWidget_genresList.item(selected_index)
            genre = item.data(Qt.ItemDataRole.UserRole)
            self.movieconn.connect()
            self.movieslist = self.movieconn.GetMoviesbyGenre(genre.genres)
            for p in self.movieslist:
                print(p)
            self.show_movie_list_on_qtable()
            self.current_selected_genre = genre
        except:
            traceback.print_exc()

    def show_movie_list_on_qtable(self):
        try:
            self.tableWidget_moviesList.setRowCount(0)
            for p in self.movieslist:
                row_index = self.tableWidget_moviesList.rowCount()
                self.tableWidget_moviesList.insertRow(row_index)

                movieId_col = QTableWidgetItem(str(p.movieId))
                title_col = QTableWidgetItem(str(p.title))
                release_year_col = QTableWidgetItem(str(p.release_year))
                genres_col = QTableWidgetItem(str(p.genres))

                self.tableWidget_moviesList.setItem(row_index, 0, movieId_col)
                self.tableWidget_moviesList.setItem(row_index, 1, title_col)
                self.tableWidget_moviesList.setItem(row_index, 2, release_year_col)
                self.tableWidget_moviesList.setItem(row_index, 3, genres_col)
        except:
            traceback.print_exc()

    def show_movie_details(self):
        selected_index = self.tableWidget_moviesList.currentRow()
        if selected_index == -1 or selected_index >= len(self.movieslist):
            return
        movieId = self.tableWidget_moviesList.item(selected_index, 0).text()
        self.movieconn.connect()
        movie = self.movieconn.GetDetail(movieId)
        if movie != None:
            self.textBrowser_movieId.setText(str(movie.movieId))
            self.textBrowser_title.setText(str(movie.title))
            self.textBrowser_releaseyears.setText(movie.release_year)
            self.textBrowser_genres.setText(str(movie.genres))
            self.textBrowser_averagerating.setText(str(movie.average_rating))

    def switch_recommend_window(self):
        try:
            print(f"Current user ID in homepageExt before switching: {self.current_user_id}")

            self.MainWindow.hide()
            self.mainwindow = QMainWindow()
            self.myui = recommendExt(user_connector=self.userconn, user_id=self.current_user_id)  # Truyền user_connector
            self.myui.setupUi(self.mainwindow)
            self.myui.showWindow()
        except:
            traceback.print_exc()

    def switch_statistic_window(self):
        try:
            self.MainWindow.hide()
            self.mainwindow = QMainWindow()
            self.myui = statisticExt(user_connector=self.userconn, user_id=self.current_user_id)  # Truyền đúng connector
            self.myui.setupUi(self.mainwindow)
            self.myui.showWindow()
        except Exception as e:
            traceback.print_exc()




