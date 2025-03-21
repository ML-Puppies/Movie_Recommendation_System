# Thông tin kết nối MySQL (thay đổi theo thông tin của bạn)
from K22416C.FINAL.Connectors.Connector import Connector
# Thông tin kết nối MySQL (thay đổi theo thông tin của bạn)
server = "localhost"
port = 3306
database = "movie_ratings"
username = "root"
password = "@Obama123"

# Khởi tạo đối tượng Connector
db_connector = Connector(server, port, database, username, password)

# Kết nối tới MySQL
connection = db_connector.connect()

if connection:
    print("✅ Kết nối thành công!")

    # Lấy danh sách bảng
    tables = db_connector.getTablesName()
    print("Danh sách bảng:", tables)

    # Nếu có ít nhất một bảng, thử truy vấn dữ liệu


