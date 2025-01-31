import numpy as np

from .model import Model


ALLOWED_METHODS = ["gini", "entropy"]


class DecisionTree(Model):
    @classmethod
    def _gini(cls, feat: np.ndarray):
        classes, counts = np.unique(feat, return_counts=True)
        probabilities = counts / len(feat)
        gini = 1 - np.sum(probabilities**2)
        return gini

    @classmethod
    def _entropy(cls, feat: np.ndarray):
        classes, counts = np.unique(feat, return_counts=True)
        probabilities = counts / len(feat)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-9))
        return entropy

    def __init__(self, method: str = "gini", max_depth: int = np.inf):
        if method not in ALLOWED_METHODS:
            raise ValueError(f"Invalid method! Allowed methods: {ALLOWED_METHODS}")
        self.impurity = self._gini if method == "gini" else self._entropy
        self.tree = None
        self.max_depth = max_depth

    def _information_gain(self, feat: np.ndarray, left_idx: int, right_idx: int):
        parent_impurity = self.impurity(feat)
        n = len(feat)
        n_left, n_right = len(left_idx), len(right_idx)

        weighted_avg = (n_left / n) * self.impurity(feat[left_idx]) + (
            n_right / n
        ) * self.impurity(feat[right_idx])
        return parent_impurity - weighted_avg

        return parent_impurity - weighted_avg

    def _best_split(self, X: np.ndarray, y: np.ndarray):
        best_gain = -1
        best_split = None

        for feature_idx in range(X.shape[1]):
            thresholds = np.unique(X[:, feature_idx])
            for threshold in thresholds:
                left_idx = np.where(X[:, feature_idx] <= threshold)[0]
                right_idx = np.where(X[:, feature_idx] > threshold)[0]

                if len(left_idx) == 0 or len(right_idx) == 0:
                    continue

                gain = self._information_gain(y, left_idx, right_idx)

                if gain > best_gain:
                    best_gain = gain
                    best_split = {
                        "feature_idx": feature_idx,
                        "threshold": threshold,
                        "left_idx": left_idx,
                        "right_idx": right_idx,
                    }

        return best_split

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int):
        if len(np.unique(y)) == 1 or (self.max_depth and depth >= self.max_depth):
            return {"value": np.bincount(y).argmax()}

        split = self._best_split(X, y)
        if not split:
            return {"value": np.bincount(y).argmax()}

        left_subtree = self._build_tree(
            X[split["left_idx"]], y[split["left_idx"]], depth=depth + 1
        )
        right_subtree = self._build_tree(
            X[split["right_idx"]], y[split["right_idx"]], depth=depth + 1
        )

        return {
            "feature_idx": split["feature_idx"],
            "threshold": split["threshold"],
            "left": left_subtree,
            "right": right_subtree,
        }

    def fit(self, X: np.ndarray, y: np.ndarray, *args, **kwargs):
        self.tree = self._build_tree(X, y, depth=0)

    def _predict_single(self, x: np.ndarray, tree: dict):
        if "value" in tree:
            return tree["value"]

        feature_value = x[tree["feature_idx"]]
        if feature_value <= tree["threshold"]:
            return self._predict_single(x, tree["left"])
        else:
            return self._predict_single(x, tree["right"])

    def predict_one(self, X: np.ndarray, *args, **kwargs):
        return self._predict_single(X, self.tree)


def test_decision_tree():
    X = np.array([[2, 3], [9, 1], [3, 7], [6, 5], [7, 8], [8, 6]])
    y = np.array([0, 0, 0, 1, 1, 1])
    print(f"Expected values: {y}")

    for method in ALLOWED_METHODS:
        tree = DecisionTree(method=method, max_depth=2)
        tree.fit(X, y)
        predictions = tree.predict(X)
        print(f"Predictions {method}: {predictions}")
        print(f"Tree {method}: {tree.tree}")


if __name__ == "__main__":
    test_decision_tree()
