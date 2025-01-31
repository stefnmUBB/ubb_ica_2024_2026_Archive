from dataloader import OccupancyEstimationDataloader
from preprocessor import DateAndTimePreprocessor
import numpy as np, scipy.stats as st
import shap

class CrossValidation:
    def __init__(self, X, Y, n_folds=10):   
        fold_size = len(X)//n_folds
        self.folds = [ (X[fold_size*i:fold_size*(i+1)], Y[fold_size*i:fold_size*(i+1)]) for i in range(n_folds)]
    
    def get_fold_iteration(self, k):
        x_test, y_test = self.folds[k]
        x_train, y_train = [], []
        
        for i in range(len(self.folds)):
            if i==k: continue
            x_train.append(self.folds[i][0])
            y_train.append(self.folds[i][1])
        
        x_train = np.concatenate(x_train, axis=0)
        y_train = np.concatenate(y_train, axis=0)
        
        return x_train, y_train, x_test, y_test

    def for_each_fold(self, action:callable):
        for k in range(len(self.folds)):
            x_train, y_train, x_test, y_test = self.get_fold_iteration(k)
            action(x_train, y_train, x_test, y_test, k)
            
    def for_one_fold(self, action:callable, k=0):
        x_train, y_train, x_test, y_test = self.get_fold_iteration(k)
        action(x_train, y_train, x_test, y_test, k)
    
class HyperParameter:
    def __init__(self, key:str, values:list):        
        self.key = key       
        # imply discrete grid-search optimization
        self.values = values 
        self.value_index = 0
    
    def get_current_value(self): return self.values[self.value_index]
    
    def advance_index(self)->bool:
        if self.value_index == len(self.values)-1:
            self.value_index = 0
            return True
        self.value_index += 1
        return False
    
    def reset_index(self): self.value_index=0
        

class HyperParameters:
    def __init__(self, params:list[HyperParameter]):
        self.params:list[HyperParameter] = params
        
    def add_param(self, param:HyperParameter):
        self.params.append(param)

    def get_current_config(self):
        return { p.key:p.get_current_value() for p in self.params }
        
    def iterate_configs(self):
        for param in self.params: param.reset_index()
        stack = [self.params[0]]
        
        while len(stack)>0:
            while len(stack)<len(self.params):
                stack.append(self.params[len(stack)])
                
            yield self.get_current_config()
            
            while len(stack)>0 and stack[-1].advance_index():
                stack.pop()
   

class MetricEstimate:
    def __init__(self, values):
        self.values = np.array(values)
        self.mean = np.mean(self.values)
        self.std = np.std(self.values)
        self.conf_interval = st.t.interval(0.95, len(self.values)-1, loc=self.mean, scale=st.sem(self.values))

    def __repr__(self):
        return f"{{ mean={self.mean}, std={self.std}, conf_interval={self.conf_interval} }}"
        
class PredictionMetrics:
    def __init__(self, metrics:dict[str, callable], best_measure:tuple[str,str]):
        self.metrics = metrics
        self.best_measure = best_measure
        
    def keys(self): return self.metrics.keys()
        
    def apply(self, y_true, y_pred):
        return { name : fun(y_true, y_pred) for name, fun in self.metrics.items() }
        
    def is_better(self, old_m:dict[str, MetricEstimate]|None, new_m:dict[str, MetricEstimate])->bool:
        if old_m is None: return True
        
        metric_name, comp = self.best_measure
        
        old_v = old_m[metric_name].mean
        new_v = new_m[metric_name].mean
        
        if comp=='max': return new_v > old_v
        return new_v < old_v
        
    @staticmethod
    def regression_metrics():
        return PredictionMetrics({
            'mae' : lambda y_true, y_pred: np.mean(np.abs(y_true-y_pred)),
            'rmse' : lambda y_true, y_pred: np.sqrt(np.mean(np.square(y_true-y_pred))),
            'nrmse' : lambda y_true, y_pred: np.sqrt(np.sum(np.square(y_true-y_pred)) / np.sum(np.square(y_true))),
            'r2' : lambda y_true, y_pred: 1 -  np.sum(np.square(y_true-y_pred)) / np.sum(np.square(y_true-np.mean(y_true)))
        }, best_measure = ('r2', 'max'))
        
        
    @staticmethod
    def classification_metrics():
        def conf_mat(y_true, y_pred, action):
            TP = ((y_pred == 1) & (y_true == 1)).sum()
            FP = ((y_pred == 1) & (y_true == 0)).sum()
            TN = ((y_pred == 0) & (y_true == 0)).sum()
            FN = ((y_pred == 0) & (y_true == 1)).sum()
            return action(TP, FP, TN, FN)
            
        return PredictionMetrics({
            'accuracy' : lambda y_true, y_pred: conf_mat(y_true, y_pred, lambda TP, FP, TN, FN: (TP+TN)/(TP+TN+FP+FN)),
            'precision' : lambda y_true, y_pred: conf_mat(y_true, y_pred, lambda TP, FP, TN, FN: TP/(TP+FP)),
            # ...
        }, best_measure = ('accuracy', 'max'))
        
        
class ModelRunner:
    def __init__(self, dataset_path:str):
        loader = OccupancyEstimationDataloader(dataset_path, DateAndTimePreprocessor.process)
        self.columns = columns = loader.input_columns
        
        X, Y = [], []        
        for _x, _y in loader: 
            X.append([_x[col] for col in columns])
            Y.append(1 if _y>0 else 0)
        X, Y = np.array(X), np.array(Y)

        
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        self.X, self.Y = X[indices], Y[indices]
        self.X, self.Y = self.X[:1000], self.Y[:1000]
        print(self.X.shape, self.Y.shape)
        
        self.cross_validation = CrossValidation(self.X, self.Y)
    
    def run(self, model_type: type, hp:HyperParameters, metrics: PredictionMetrics):
        def perform_cv(hp_cfg):
            metric_vals = { key:[] for key in metrics.keys() }            
            def process_fold(x_train, y_train, x_test, y_test, k):
                print(f"Fold {k}")
                model = model_type(**hp_cfg)
                model.fit(x_train, y_train)            
                y_pred = model.predict(x_test)            
                m_vals = metrics.apply(y_test, y_pred)
                print(m_vals)
                
                for key, value in m_vals.items():
                    metric_vals[key].append(value)                
                
            self.cross_validation.for_each_fold(process_fold)
    
            for key in metric_vals.keys():
                metric_vals[key] = MetricEstimate(metric_vals[key])
           
            return metric_vals
    
        best_hp_cfg = {}
        best_metrics = None
        
        for hp_cfg in hp.iterate_configs():
            print(f"Hyperparams = {hp_cfg}")
            metric_vals = perform_cv(hp_cfg)
            if metrics.is_better(best_metrics, metric_vals):
                best_metrics = metric_vals
                best_hp_cfg = hp_cfg
                
        
        return best_hp_cfg, best_metrics
            
            
        
    def shap(self, model_type, params, pred_caller=lambda x:x):
        model = model_type(**params)
        
        ex_train = []
        ex_test = []
        ey_test = []
        
        def process_fold(x_train, y_train, x_test, y_test, k):      
                nonlocal ex_test, ey_test
                model.fit(x_train, y_train)  
                ex_test = x_test
                ey_test = y_test
        
        self.cross_validation.for_one_fold(process_fold)
        
    
        def masker(mask, x): return x.reshape(1, -1)
    
        explainer = shap.Explainer(pred_caller(model), masker, feature_names=self.columns, )
        shap_values = explainer(ex_test)
        shap.waterfall_plot(shap_values[0])
        
        
        
        
    
        
    