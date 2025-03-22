import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.sparse import csr_matrix
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
        self.Ybar = None 

    def load_data_and_process(self):
        """Load and process data through Preprocess.py"""
        self.load_data()
        self.process()
        df_movies, df_ratings = self.get_dataframes()
        df = df_ratings.merge(df_movies, on='movieId', how='left')
        return df[['userId', 'movieId', 'rating']].values

    def processTrain(self, test_size=0.2, random_state=42):
        """Split the data into training and testing sets."""
        data_matrix = self.load_data_and_process()
        self.user_map = {user: idx for idx, user in enumerate(np.unique(data_matrix[:, 0]))}
        self.item_map = {item: idx for idx, item in enumerate(np.unique(data_matrix[:, 1]))}
        self.n_users = len(self.user_map)
        self.n_items = len(self.item_map)
        self.Y_data = np.array([[self.user_map[u], self.item_map[i], r] for u, i, r in data_matrix])

        # Check the size of the data
        print(f"Training data size: {self.Y_data.shape[0]}")

        self.Ybar = self._prepare_matrix()  # Khởi tạo Ybar sau khi xử lý dữ liệu
        self.X_train, self.X_test = train_test_split(self.Y_data, test_size=test_size, random_state=random_state)
        print(f"Train size: {self.X_train.shape[0]}, Test size: {self.X_test.shape[0]}")

        self.fit()

    def fit(self):
        """Train the KNN model."""
        if self.Ybar is None:
            raise ValueError("Ybar is not initialized.")
        Ybar_sparse, self.mu = self.Ybar
        knn = NearestNeighbors(n_neighbors=min(self.k, self.n_users), metric='cosine', algorithm='auto', n_jobs=-1)
        knn.fit(Ybar_sparse)
        self.S_distances, self.S_indices = knn.kneighbors(Ybar_sparse, return_distance=True)
        self.model = knn
        print("Model trained successfully!")

    def _prepare_matrix(self):
        """Convert the data into a matrix suitable for KNN."""
        users = self.Y_data[:, 0].astype(int)
        mu = np.zeros(self.n_users)
        for n in range(self.n_users):
            idx = np.where(users == n)[0]
            ratings = self.Y_data[idx, 2]
            if len(ratings) > 0:
                mu[n] = np.mean(ratings)
        return csr_matrix((self.Y_data[:, 2], (users, self.Y_data[:, 1].astype(int)))), mu

    def predict(self, u, i):
        """Predict the rating for user u and movie i."""
        if not isinstance(u, int) or not isinstance(i, int) or u >= self.n_users or i >= self.n_items:
            return np.mean(self.mu)

        if self.uuCF:
            nearest_neighbors = self.S_indices[u]
        else:
            nearest_neighbors = self.S_indices[i]

        valid_neighbors = np.array([n for n in nearest_neighbors if 0 <= n < self.n_users], dtype=int)

        if valid_neighbors.size == 0:
            return self.mu[u]

        Ybar_dense = self.Ybar[0].toarray()
        r = Ybar_dense[valid_neighbors, i]
        sim = self.S_distances[u][:len(valid_neighbors)]

        predicted_rating = (r * sim).sum() / (np.abs(sim).sum() + 1e-8) + self.mu[u]
        return np.clip(predicted_rating, 0, 5)

    def recommend(self, u):
        """
        Recommend movies for user u.

        This function will find movies that user u has not rated, then predict the rating for those movies
        based on movies that similar users have rated. Finally, it will return a list of recommended movies
        sorted by predicted rating from highest to lowest.

        Parameters:
        u (int): The ID of the user we want to recommend movies for.

        Returns:
        list: A list of the top 10 recommended movies for user u, sorted by predicted rating.
        """

        if u >= self.n_users:
            print(f"User {u} does not exist in the dataset.")
            return []

        # Get the movies that user u has rated
        rated_items = set(self.Y_data[self.Y_data[:, 0] == u][:, 1])
        recommendations = []

        # Iterate through all movies in the dataset
        for i in range(min(self.n_items, 300)):  # Limit to a maximum of 300 movies
            if i not in rated_items:  # If the movie has not been rated by user u
                rating = self.predict(u, i)  # Predict the rating for movie i by user u
                recommendations.append((i, rating))  # Add the movie and predicted rating to the list

        # Sort the list by predicted rating from highest to lowest and return the top 10
        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]

    def evaluate(self):
        """Evaluate the model on the test set."""
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
        return metrics
