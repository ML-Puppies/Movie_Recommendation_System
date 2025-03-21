from K22416C.FINAL.Connectors.Connector import Connector
from K22416C.FINAL.Models.CollaborativeFiltering import MovieCollaborativeFiltering


def test_collaborative_filtering():
    # Kết nối database
    connector = Connector()
    connector.connect()

    # Tạo đối tượng Collaborative Filtering
    cf_model = MovieCollaborativeFiltering(connector, k=10, uuCF=True)

    print("🔍 Bắt đầu quá trình huấn luyện mô hình...")
    cf_model.processTrain()
    print("✅ Huấn luyện mô hình thành công!")

    # Kiểm tra dự đoán
    sample_prediction = cf_model.predict(13, 13)
    print("🎯 Dự đoán rating cho user 0 và movie 0:", sample_prediction)

    # Kiểm tra đề xuất phim
    try:
        recommendations = cf_model.recommend(0)
        print("🎥 Top phim được đề xuất cho user 0:", recommendations)
    except IndexError as e:
        print(f"❌ Lỗi khi đề xuất phim: {e}")

    # Kiểm tra đánh giá mô hình
    evaluation_metrics = cf_model.evaluate()
    print("📊 Đánh giá mô hình:", evaluation_metrics)

    # Đóng kết nối
    connector.disConnect()
    print("🔌 Đã đóng kết nối database.")


if __name__ == "__main__":
    test_collaborative_filtering()
