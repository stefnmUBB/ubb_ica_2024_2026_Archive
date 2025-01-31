from src.model_runner import (
    ModelRunner,
    HyperParameter,
    HyperParameters,
    PredictionMetrics,
)
from src.hyperparameters import hyperparams_svr
from src.model_runner import ModelRunner
from src.models import MySVR

from sklearn.svm import SVR


def pred_caller(svr):
    def f(x_test):
        return svr.predict(x_test)

    return f


if __name__ == "__main__":
    model_type = SVR
    ds_path = r"D:\anu1m\sem1\roe_ds\Occupancy_Estimation.csv"

    runner = ModelRunner(ds_path)
    # hp_cfg, metrics = runner.run(model_type, hyperparams_svr, PredictionMetrics.regression_metrics())

    print("Done.")
    # print("Optimized hyperparameters:\n", hp_cfg)
    # print("Metrics:\n", metrics)

    runner.shap(
        model_type, hyperparams_svr.get_current_config(), pred_caller=pred_caller
    )

    """
    sklearn SVR result
     {'kernel': 'poly', 'degree': 2, 'C': 1.0, 'epsilon': 0.01, 'tol': 0.01}
    Metrics:
     {'mae': { mean=0.05812253529103369, std=0.007888263065000158, conf_interval=(0.05217437169300859, 0.0640706988890588) }, 
     'rmse': { mean=0.19163508171063265, std=0.02437511921430278, conf_interval=(0.17325496486953246, 0.21001519855173284) }, 
     'nrmse': { mean=0.31804111771478255, std=0.03793311415504675, conf_interval=(0.2894375624178123, 0.3466446730117528) }, 
     'r2': { mean=0.8386224413550899, std=0.038404801298356626, conf_interval=(0.8096632092415159, 0.8675816734686639) }}
    """
