import numpy as np
from .QP import QPSolver
from .model import Model

class KernelProvider:
    def __init__(self, x, kerf):
        self.kerf = kerf        
        self.n = len(x)
        
        self._K = []        
        
        for i in range(len(x)):
            row = []
            for j in range(0, i+1):
                row.append(kerf(x[i], x[j]))
            self._K.append(row)
    
    def K(self, i, j):
        sgn = 1
        if i>=self.n: sgn*=-1; i-=self.n
        if j>=self.n: sgn*=-1; j-=self.n
        if i<j: i,j = j,i
        return sgn * self._K[i][j]
    
    def K_new(self, x, y): return self.kerf(x, y)
    
    def __getitem__(self, pos): 
        return self.K(*pos)
    
    
class Kernels:
    @staticmethod
    def linear():        
        return lambda x,y: x @ y        
    
    @staticmethod
    def poly(c0): 
        def f(x, y):
            z = np.atleast_1d(x @ y + c0)
            return z @ z
        return f
    
def solve_qp(K, P, C, A, x0):
    """
        min 1/2 x^t*K*x + P*x, s.t. 0<=x<=C && A*x=0
        knowing x0 initial feasable solution
    """
    n = len(P)

    def xKx(x):
        # Computes x^t * K * x aka sum(k_ij * x_i * x_j) => real number 
        res = 0
        for i in range(len(x)):
            for j in range(len(x)):
                res += K[i,j] * x[i] * x[j]
        return res
    
    def Kx(x):
        # Computes K*x => vector with shape of x
        res = np.zeros(len(x))
        for i in range(len(x)):
            for j in range(len(x)):
                res[i] += K[i,j]*x[j]
        return res
    
    def fun(x):
        # Objective function: 1/2 x^t*K*x + P*x
        return 0.5 * xKx(x) + P @ x        

    def dfun(x):
        # Gradient of the objective function: K*x + P
        return Kx(x) + P        

    def cons(x):
        # Constraint functions: equality A*x = 0 and 0<=x<=C <=> x>=0, C-x>=0
        h = np.array([ A @ x ])
        g = np.concatenate([ x, C-x ], axis=0)        
        return h, g

    def dcons(x):
        # Jacobi matrix of constraint functions
        Ae = A.reshape((1, -1))
        Ai = np.concatenate([np.eye(len(x)), -np.eye(len(x))], axis=0)
        return Ae, Ai

    # dual variables associated the equality constraint
    mu0 = np.zeros(1)  
    # dual variables associated with inequality constraints
    lam0 = np.zeros(2*n) 
    # optimize problem
    x_op, mu_op, lam_op, fval = QPSolver.solve_SQP(fun, dfun, cons, dcons, x0, mu0, lam0, True)
    
    return x_op
    

class MySVR(Model):
    def __init__(self,
        epsilon=1e-2,
        kernel='linear',
        degree=2,
        coef0=0,
        C=1
    ):
        self.epsilon = epsilon
        self.C = C
                
        if kernel=='linear':
            self.kerf = Kernels.linear()
        elif kernel=='poly':
            assert degree==2
            self.kerf = Kernels.poly(coef0)
        else:
            raise ValueError(f"Invalid kernel: {kernel}")
    
    
    def fit(self, x: np.ndarray, y: np.ndarray, *args, **kwargs):
        n = len(x)
        self.kp = kp = KernelProvider(x, self.kerf)
        p = np.concatenate([-y + self.epsilon, y + self.epsilon], axis=0)
        
        a = np.concatenate([np.ones(n), -np.ones(n)])
        
        alpha = solve_qp(self.kp, p, self.C, a, np.zeros(2*n))
    
        support_vectors_indices = []        
        coeffs = []
        
        low = min(abs(alpha))
        for i in range(n):
            if abs(alpha[i]-alpha[n+i]) >= low+self.epsilon:
                support_vectors_indices.append(i)
                coeffs.append(alpha[i]-alpha[n+i])
                
        coeffs = np.array(coeffs)
        
        def coeff_k_prod(coeffs, support_vectors_indices, x_index):
            res = 0
            for i in range(len(coeffs)):
                res += coeffs[i] * self.kp.K(support_vectors_indices[i], x_index)
            return res
        
        bias = 0
        for i in range(n):
            bias += y[i] - self.epsilon - coeff_k_prod(coeffs, support_vectors_indices, i)
        bias /= n
        
        self.coeffs = coeffs
        self.bias = bias
        self.support_vectors = np.array([x[i] for i in support_vectors_indices])
        
        #print(self.coeffs)
        #print(self.bias)
        #print(self.support_vectors)
    
    def predict(self, x: np.ndarray, *args, **kwargs) -> np.ndarray: 
        def coeff_k_prod(x):
            res = 0
            for i in range(len(self.coeffs)):
                res += self.coeffs[i] * self.kp.K_new(self.support_vectors[i], x)
            return res
    
        y = []
        for i in range(len(x)):            
            y.append(coeff_k_prod(x[i]) + self.bias)
            S = 0
            for j in range(len(self.coeffs)):
                S += self.coeffs[j] * ((self.support_vectors[j] @ x[i]) ** 2)
            
        return np.array(y)
    
    def predict_one(self, X: np.ndarray, *args, **kwargs) -> np.ndarray:
        return self.predict(X.reshape(1, -1))[0]        