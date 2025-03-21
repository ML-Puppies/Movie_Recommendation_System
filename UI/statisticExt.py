import matplotlib
matplotlib.use("QtAgg")  # Đảm bảo dùng backend tương thích với PyQt
from PyQt6 import QtWidgets
from K22416C.FINAL.Models.MoviesStatistic import MoviesStatistic
from K22416C.FINAL.UI.statistic import Ui_MainWindow
from K22416C.FINAL.Models.Preprocess import Preprocessing
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class statisticExt(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.connector.connect()  # Đảm bảo có kết nối trước khi truy vấn
        self.movies_statistic = MoviesStatistic(self.connector)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        super().setupUi(self)
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        # Gán sự kiện cho các nút bấm
        self.pushbuttonTop10MBR.clicked.connect(self.show_top_10_movies_by_ratings)
        self.pushbuttonTop10GBR.clicked.connect(self.show_top_genres_by_ratings)
        self.pushbutton5star.clicked.connect(self.show_top_10_movies_with_5_stars)
        self.pushbuttonTop10MRLY.clicked.connect(self.show_top_10_most_rated_movies_last_year)
        self.pushbuttonTopGOVT.clicked.connect(self.show_top_genres_over_time)
        self.pushbuttonTop10MRG.clicked.connect(self.show_top_10_movies_by_most_rated_genre)

    def showWindow(self):
        self.MainWindow.show()

    def show_top_10_movies_by_ratings(self):
        try:
            figure = self.movies_statistic.top_10_movies_by_ratings(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("⚠ Không thể tạo biểu đồ, có thể dữ liệu bị lỗi!")
        except Exception as e:
            print(f"⚠ Lỗi khi hiển thị biểu đồ: {e}")

    def show_top_genres_by_ratings(self):
        try:
            figure = self.movies_statistic.top_genres_by_ratings(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("⚠ Không thể tạo biểu đồ, có thể dữ liệu bị lỗi!")
        except Exception as e:
            print(f"⚠ Lỗi khi hiển thị biểu đồ: {e}")

    def show_top_10_movies_with_5_stars(self):
        try:
            figure = self.movies_statistic.top_10_movies_with_5_stars(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("⚠ Không thể tạo biểu đồ, có thể dữ liệu bị lỗi!")
        except Exception as e:
            print(f"⚠ Lỗi khi hiển thị biểu đồ: {e}")

    def show_top_10_most_rated_movies_last_year(self):
        try:
            figure = self.movies_statistic.top_10_most_rated_movies_last_year(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("⚠ Không thể tạo biểu đồ, có thể dữ liệu bị lỗi!")
        except Exception as e:
            print(f"⚠ Lỗi khi hiển thị biểu đồ: {e}")

    def show_top_genres_over_time(self):
        try:
            figure = self.movies_statistic.top_genres_over_time(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("⚠ Không thể tạo biểu đồ, có thể dữ liệu bị lỗi!")
        except Exception as e:
            print(f"⚠ Lỗi khi hiển thị biểu đồ: {e}")


    def show_top_10_movies_by_most_rated_genre(self):
        try:
            figure = self.movies_statistic.top_10_movies_by_most_rated_genre(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("⚠ Không thể tạo biểu đồ, có thể dữ liệu bị lỗi!")
        except Exception as e:
            print(f"⚠ Lỗi khi hiển thị biểu đồ: {e}")

    def show_plot(self, figure):
        """ Hiển thị biểu đồ trong verticalLayoutPlot """
        # Xóa widget cũ trong layout nếu có
        for i in reversed(range(self.verticalLayoutPlot.count())):
            widget = self.verticalLayoutPlot.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Tạo canvas từ Figure và thêm vào layout
        canvas = FigureCanvas(figure)
        self.verticalLayoutPlot.addWidget(canvas)
