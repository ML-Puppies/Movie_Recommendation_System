from PyQt6.QtWidgets import QMessageBox
import pandas as pd
from sqlalchemy import create_engine
from loginmyfilm import Ui_MainWindow  # Giao diện UI của Login
from homepage import MainWindow  # Giao diện UI của Homepage

class LoginWindow(Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Thông tin kết nối MySQL
        self.user = "root"
        self.password = "Giang0409$"
        self.host = "localhost"
        self.database = "movie_ratings"

        self.engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}")
        self.setupUi(self)  # Khởi tạo giao diện

    def login(self, user_id, password):
        try:
            # Truy vấn kiểm tra thông tin đăng nhập trong bảng users
            query = f"SELECT * FROM users WHERE userID = {user_id} AND password = '{password}'"
            df = pd.read_sql(query, self.engine)

            # Nếu có kết quả trả về, đăng nhập thành công
            if not df.empty:
                return True
            else:
                return False
        except Exception as e:
            print(f"Đã có lỗi xảy ra: {e}")
            return False

    def handle_login(self):
        user_id = self.lineEdit.text()  # Lấy UserID từ giao diện
        password = self.lineEdit_2.text()  # Lấy mật khẩu từ giao diện

        if self.login(user_id, password):
            self.result_label.setText("Đăng nhập thành công!")
            self.open_main_window()  # Chuyển đến trang chủ sau khi đăng nhập thành công
        else:
            self.result_label.setText("Đăng nhập thất bại!")
            self.show_error_message()  # Hiển thị thông báo lỗi

    def open_main_window(self):
        # Tạo và hiển thị cửa sổ Homepage sau khi đăng nhập thành công
        self.main_window = MainWindow() 
        self.main_window.show()
        self.close()  # Đóng cửa sổ đăng nhập

    def show_error_message(self):
        # Hiển thị thông báo lỗi khi đăng nhập thất bại
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Icon.Critical)
        error_msg.setText("Đăng nhập thất bại!")
        error_msg.setInformativeText("Vui lòng kiểm tra lại UserID và mật khẩu.")
        error_msg.setWindowTitle("Lỗi")
        error_msg.exec()
