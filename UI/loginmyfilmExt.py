import traceback

from PyQt6.QtWidgets import QMessageBox, QMainWindow

from K22416C.FINAL.Connectors.User_Connector import UserConnector
from K22416C.FINAL.UI.loginmyfilm import Ui_MainWindow
from K22416C.FINAL.UI.homepageExt import homepageExt


class loginmyfilmExt(Ui_MainWindow):
    def __init__(self):
        self.userconn = UserConnector()  # Initialize the user connector

    def setupUi(self, MainWindow):
        """ Set up the login UI and signals """
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()

    def showWindow(self):
        """ Show the login window """
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        """ Connect login button to login function """
        self.pushButton_Login.clicked.connect(self.login_process)

    def login_process(self):
        """ Handle user login and navigate to the "homepage" if successful """
        try:
            userID=self.lineEdit_InputUserID.text()
            password=self.lineEdit_InputPassword.text()

            # Connect to the database and attempt login
            self.userconn.connect()
            self.userlogin = self.userconn.login(userID, password)

            if self.userlogin is not None:
                self.MainWindow.hide()
                self.mainwindow = QMainWindow()

                current_user_id = self.userlogin.userId  # Access the userId from the User object
                print(f"Current User ID after login: {current_user_id}")

                # Open homepage with user session
                self.myui = homepageExt(user_connector=self.userconn, user_id=current_user_id)  # Truyền user_connector vào homepageExt
                self.myui.setupUi(self.mainwindow)
                self.myui.showWindow()

            else:
                # Show error message if login fails
                self.msg=QMessageBox()
                self.msg.setWindowTitle("Login Failed")
                self.msg.setText("Login unsuccessful.\nPlease check your credentials.")
                self.msg.setIcon(QMessageBox.Icon.Critical)
                self.msg.show()
        except:
            traceback.print_exc()