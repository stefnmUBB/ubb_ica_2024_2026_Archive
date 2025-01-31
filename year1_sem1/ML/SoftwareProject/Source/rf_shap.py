from sklearn.ensemble import RandomForestClassifier

from src.model_runner import ModelRunner
from src.models import RandomForest as MyRandomForest, Model


if __name__ == "__main__":
    runner = ModelRunner("dataset/Occupancy_Estimation.csv")

    def pred_caller(rf: Model):
        def f(x_test):
            return rf.predict(x_test)

        return f

    hp_cfg = {
        "criterion": "gini",
        "n_estimators": 20,
        "max_depth": 5,
        "max_features": 5,
    }
    runner.shap(MyRandomForest, hp_cfg, pred_caller=pred_caller)

    library_hp_cfg = {
        "criterion": "entropy",
        "n_estimators": 20,
        "max_depth": 3,
        "max_features": 5,
    }

    runner.shap(RandomForestClassifier, library_hp_cfg, pred_caller=pred_caller)
