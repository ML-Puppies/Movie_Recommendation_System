import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from K22416C.FINAL.Models.Preprocess import Preprocessing


class MetricsResult:
    def __init__(self, mae, mse, rmse, r2):
        self.mae = mae
        self.mse = mse
        self.rmse = rmse
        self.r2 = r2

    def __repr__(self):
        return f"MetricsResult(MAE={self.mae}, MSE={self.mse}, RMSE={self.rmse}, R2={self.r2})"


class MovieCollaborativeFiltering(Preprocessing):
    def __init__(self, connector=None, k=20, uuCF=True):
        super().__init__(connector)
        self.k = min(k, 10)
        self.uuCF = uuCF
        self.model = None
        self.user_map = {}
        self.item_map = {}
        self.n_users = 0
        self.n_items = 0

    def load_data_and_process(self):
        print("🔍 Đang tải và xử lý dữ liệu...")
        self.load_data()
        self.process()
        df_movies, df_ratings = self.get_dataframes()
        if df_movies is None or df_ratings is None:
            raise ValueError("❌ Lỗi: Dữ liệu movies hoặc ratings bị None sau khi process!")
        df = df_ratings.merge(df_movies, on='movieId', how='left')
        return df[['userId', 'movieId', 'rating']].values

    def processTrain(self, test_size=0.2, random_state=42):
        data_matrix = self.load_data_and_process()
        if data_matrix is None or len(data_matrix) == 0:
            raise ValueError("❌ Lỗi: Dữ liệu huấn luyện trống!")

        self.user_map = {user: idx for idx, user in enumerate(np.unique(data_matrix[:, 0]))}
        self.item_map = {item: idx for idx, item in enumerate(np.unique(data_matrix[:, 1]))}

        self.n_users = len(self.user_map)
        self.n_items = len(self.item_map)

        print(f"👤 Tổng số user: {self.n_users}, 🎥 Tổng số phim: {self.n_items}")

        self.Y_data = np.array([[self.user_map[u], self.item_map[i], r] for u, i, r in data_matrix])
        self.Ybar = self._normalize_matrix()

        self.X_train, self.X_test = train_test_split(self.Y_data, test_size=test_size, random_state=random_state)
        self.fit()

    def _normalize_matrix(self):
        users = self.Y_data[:, 0].astype(int)
        mu = np.zeros(self.n_users)

        for n in range(self.n_users):
            idx = np.where(users == n)[0]
            ratings = self.Y_data[idx, 2]
            if len(ratings) > 0:
                mu[n] = np.mean(ratings)
                min_r, max_r = np.min(ratings), np.max(ratings)
                if max_r > min_r:
                    self.Y_data[idx, 2] = (ratings - min_r) / (max_r - min_r)

        return csr_matrix((self.Y_data[:, 2], (users, self.Y_data[:, 1].astype(int)))), mu

    def fit(self):
        print("🏋️ Bắt đầu train mô hình KNN...")
        Ybar_sparse, self.mu = self.Ybar
        knn = NearestNeighbors(n_neighbors=min(self.k, self.n_users), metric='cosine', algorithm='auto', n_jobs=-1)
        knn.fit(Ybar_sparse)
        self.S_distances, self.S_indices = knn.kneighbors(Ybar_sparse, return_distance=True)
        self.model = knn
        print("✅ Train mô hình thành công!")

    def predict(self, u, i):
        if not isinstance(u, int) or not isinstance(i, int) or u >= self.n_users or i >= self.n_items:
            return np.mean(self.mu)

        if self.uuCF:
            nearest_neighbors = self.S_indices[u]
        else:
            nearest_neighbors = self.S_indices[i]  # Item-Based CF

        valid_neighbors = np.array([n for n in nearest_neighbors if 0 <= n < self.n_users], dtype=int)

        if valid_neighbors.size == 0:
            return self.mu[u]

        Ybar_dense = self.Ybar[0].toarray()
        if i >= Ybar_dense.shape[1]:
            return self.mu[u]

        r = Ybar_dense[valid_neighbors, i]
        sim = self.S_distances[u][:len(valid_neighbors)]
        return (r * sim).sum() / (np.abs(sim).sum() + 1e-8) + self.mu[u]

    def recommend(self, u):
        if u >= self.n_users:
            print(f"❌ User {u} không tồn tại trong dataset.")
            return []

        rated_items = set(self.Y_data[self.Y_data[:, 0] == u][:, 1])
        recommendations = []

        for i in range(min(self.n_items, 300)):
            if i not in rated_items:
                rating = self.predict(u, i)
                recommendations.append((i, rating))

        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]

    def evaluate(self):
        actual_ratings = []
        predicted_ratings = []
        for u, i, actual_rating in self.X_test:
            predicted_rating = self.predict(int(u), int(i))
            actual_ratings.append(actual_rating)
            predicted_ratings.append(predicted_rating)

        mae = mean_absolute_error(actual_ratings, predicted_ratings)
        mse = mean_squared_error(actual_ratings, predicted_ratings)
        rmse = np.sqrt(mse)
        r2 = r2_score(actual_ratings, predicted_ratings)

        metrics = MetricsResult(mae, mse, rmse, r2)
        print("📊 Đánh giá mô hình:", metrics)
        return metrics