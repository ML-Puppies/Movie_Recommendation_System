import matplotlib.pyplot as plt
from PyQt6 import QtWidgets
from K22416C.FINAL.Models.MoviesStatistic import MoviesStatistic
from K22416C.FINAL.UI.statistic import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class statisticExt(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, connector):
        """Initializes the main window and sets up the connection and statistics object."""
        super().__init__()
        self.connector = connector
        self.connector.connect()
        self.movies_statistic = MoviesStatistic(self.connector)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        """Sets up the user interface and assigns events to buttons for displaying different plots."""
        super().setupUi(self)
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

        self.pushbuttonTop10MBR.clicked.connect(self.show_top_10_movies_by_ratings)
        self.pushbuttonTop10GBR.clicked.connect(self.show_top_genres_by_ratings)
        self.pushbutton5star.clicked.connect(self.show_top_10_movies_with_5_stars)
        self.pushbuttonTop10MRLY.clicked.connect(self.show_top_10_most_rated_movies_last_year)
        self.pushbuttonTopGOVT.clicked.connect(self.show_top_genres_over_time)
        self.pushbuttonTop10MRG.clicked.connect(self.show_top_10_movies_by_most_rated_genre)

    def showWindow(self):
        """Displays the main window."""
        self.MainWindow.show()

    def show_top_10_movies_by_ratings(self):
        """Displays the top 10 movies by ratings."""
        try:
            figure = self.movies_statistic.top_10_movies_by_ratings(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("Unable to create the plot, data might be faulty")
        except Exception as e:
            print(f"Error displaying plot: {e}")

    def show_top_genres_by_ratings(self):
        """Displays the top genres by ratings."""
        try:
            figure = self.movies_statistic.top_genres_by_ratings(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("Unable to create the plot, data might be faulty")
        except Exception as e:
            print(f"Error displaying plot: {e}")

    def show_top_10_movies_with_5_stars(self):
        """Displays the top 10 movies with 5-star ratings."""
        try:
            figure = self.movies_statistic.top_10_movies_with_5_stars(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("Unable to create the plot, data might be faulty")
        except Exception as e:
            print(f"Error displaying plot: {e}")

    def show_top_10_most_rated_movies_last_year(self):
        """Displays the top 10 most rated movies from the last year."""
        try:
            figure = self.movies_statistic.top_10_most_rated_movies_last_year(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("Unable to create the plot, data might be faulty")
        except Exception as e:
            print(f"Error displaying plot: {e}")

    def show_top_genres_over_time(self):
        try:
            figure = self.movies_statistic.top_genres_over_time(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("Unable to create the plot, data might be faulty")
        except Exception as e:
            print(f"Error displaying plot: {e}")


    def show_top_10_movies_by_most_rated_genre(self):
        """Displays the top genres over time."""
        try:
            figure = self.movies_statistic.top_10_movies_by_most_rated_genre(return_figure=True)
            if figure:
                self.show_plot(figure)
            else:
                print("Unable to create the plot, data might be faulty")
        except Exception as e:
            print(f"Error displaying plot: {e}")

    def show_plot(self, figure):
        """Displays the plot in the verticalLayoutPlot widget without cropping."""
        # Clear existing widgets in the layout if any
        for i in reversed(range(self.verticalLayoutPlot.count())):
            widget = self.verticalLayoutPlot.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Get the parent widget of the verticalLayoutPlot and its width/height
        parent_widget = self.verticalLayoutPlot.parentWidget()
        layout_width = parent_widget.width()  # Get the parent widget's width
        layout_height = parent_widget.height()  # Get the parent widget's height

        # Use plt.figure(figsize=(width, height)) to set a fixed figure size
        plt.figure(figsize=(8, 6))  # Fixed size for all plots or adjust to layout size

        # Apply tight layout to avoid clipping of plot elements
        figure.tight_layout(pad=2.0)  # Add padding to adjust spacing

        # Adjust the legend
        figure.legend(
            loc='upper left',  # Position the legend in the upper-left corner
            bbox_to_anchor=(1, 1),  # Move the legend outside the plot area
            fontsize=8,  # Set the font size smaller to reduce clutter
            title_fontsize=10,  # Title font size for the legend
            markerscale=0.8  # Adjust marker size in the legend
        )

        # Reduce the font size of axis labels and ticks to make the plot more compact
        for label in figure.get_axes():
            label.title.set_fontsize(10)  # Title font size
            label.xaxis.label.set_fontsize(9)  # X-axis label font size
            label.yaxis.label.set_fontsize(9)  # Y-axis label font size
            for tick in label.get_xticklabels():
                tick.set_fontsize(7)  # X-axis tick font size
            for tick in label.get_yticklabels():
                tick.set_fontsize(7)  # Y-axis tick font size

        # Create a canvas from the figure and add it to the layout
        canvas = FigureCanvas(figure)
        self.verticalLayoutPlot.addWidget(canvas)

        # Ensure layout is updated and resized dynamically to fit the canvas
        self.verticalLayoutPlot.update()

