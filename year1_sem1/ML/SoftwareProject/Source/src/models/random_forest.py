import math

import numpy as np

from .decision_tree import DecisionTree, ALLOWED_METHODS
from .model import Model


class RandomForest(Model):
    def __init__(
        self,
        n_estimators: int = 10,
        max_depth: int = np.inf,
        max_features: int | str | None = None,
        criterion: str = "gini",
    ):
        if criterion not in ALLOWED_METHODS:
            raise ValueError(f"Invalid method: {criterion}")

        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.method = criterion
        self.trees = []

    @classmethod
    def _bootstrap_sample(cls, X: np.ndarray, y: np.ndarray):
        n_samples = X.shape[0]
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        return X[indices], y[indices]

    def _select_features(self, X: np.ndarray):
        n_features = X.shape[1]
        max_features = self.max_features or n_features

        if max_features == "sqrt":
            max_features = int(math.sqrt(n_features))
        elif max_features == "log2":
            max_features = int(math.log2(n_features))
        elif not isinstance(max_features, int):
            raise ValueError(f"Invalid max features: {max_features}")

        feature_indices = np.random.choice(n_features, size=max_features, replace=False)
        return X[:, feature_indices], feature_indices

    def fit(self, X: np.ndarray, y: np.ndarray, *args, **kwargs):
        self.trees = []
        for _ in range(self.n_estimators):
            X_sample, y_sample = self._bootstrap_sample(X, y)
            X_sample, feature_indices = self._select_features(X_sample)

            tree = DecisionTree(method=self.method, max_depth=self.max_depth)
            tree.fit(X_sample, y_sample)

            self.trees.append((tree, feature_indices))

    def predict_one(self, X: np.ndarray, *args, **kwargs):
        tree_predictions = np.array(
            [
                tree.predict_one(X[feature_indices])
                for tree, feature_indices in self.trees
            ]
        )
        final_prediction = np.bincount(tree_predictions).argmax()  # Majority voting
        return final_prediction


def test_random_forest():
    X = np.array([[2, 3], [9, 1], [3, 7], [6, 5], [7, 8], [8, 6]])
    y = np.array([0, 0, 0, 1, 1, 1])

    print(f"Expected values: {y}")

    rf = RandomForest(n_estimators=6, max_depth=3, max_features="sqrt", method="gini")
    rf.fit(X, y)
    predictions = rf.predict(X)
    print(f"Predictions: {predictions}")
    print(f"Trees:")
    for idx, tree in enumerate(rf.trees, start=1):
        print(f"{idx}) feats: {tree[1]} - {tree[0].tree}")


if __name__ == "__main__":
    test_random_forest()
