from .model_runner import HyperParameter, HyperParameters

hyperparams_svr = HyperParameters(
    [
        HyperParameter("kernel", ["poly"]),
        HyperParameter("degree", [2]),
        HyperParameter("C", [0.1, 0.5, 1.0]),
        HyperParameter("epsilon", [1e-1, 1e-2]),
    ]
)

hyperparams_rf = HyperParameters(
    [
        HyperParameter("criterion", ["gini", "entropy"]),
        HyperParameter("n_estimators", [2, 10, 20]),
        HyperParameter("max_depth", [3, 5]),
        HyperParameter("max_features", [5, 10]),
    ]
)
