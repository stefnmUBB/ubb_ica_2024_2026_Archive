from abc import ABC

import numpy as np


class Model(ABC):
    def fit(self, X: np.ndarray, y: np.ndarray, *args, **kwargs): ...

    def predict_one(self, X: np.ndarray, *args, **kwargs) -> np.ndarray: ...

    def predict(self, X_set: np.ndarray, *args, **kwargs) -> np.ndarray:
        y = np.apply_along_axis(self.predict_one, 1, X_set, *args, **kwargs)
        return y
