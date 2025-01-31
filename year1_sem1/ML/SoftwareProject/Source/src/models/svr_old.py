import numpy as np

from .model import Model

class KernelProvider:
    def __init__(self, phi, x, u):
        self.phi = phi
        self.x = x               
        self.u = u
        self.n = len(x)
        self.cache_size=6000
        self.phi_cache = [None]*self.cache_size
    
    def __get_phi(self, i):
        if i>=self.cache_size:
            return self.phi(self.x[i])        
        if self.phi_cache[i] is None:
            self.phi_cache[i] = self.phi(self.x[i])
        return self.phi_cache[i]
        
        
    def K(self, i:int,j:int):         
        if i>=self.n: i-=self.n
        if j>=self.n: j-=self.n
        return self.__get_phi(i) @ self.__get_phi(j)
        
    def Q(self, i:int,j:int): 
        return self.u[i]*self.u[j]*self.K(i,j)

class SVR():
    def __init__(self,        
        epsilon=0.1,
        C=1.0,
        tol=0.001,
        max_iter = -1,
        kernel='linear',
        degree=2,
        coef0=0
    ):
        self.epsilon = epsilon
        self.C = C
        self.phi = lambda x:x
        self.coef0 = coef0
        self.degree = degree
        if kernel=="poly":
            if self.degree!=2:
                raise NotImplementedError("Only degree 2 polynomial kernels are implemented")
            def poly2_phi(x):
                parts = [x*x]
                pairs = np.array([[i,j] for i in range(x.shape[-1]) for j in range(x.shape[-1]) if i<j])                
                if len(pairs)>0:
                    parts.append(np.sqrt(2) * x[..., pairs[:,0]] * x[..., pairs[:, 1]],)
                parts.append(np.sqrt(2*self.coef0) * x)
                parts.append(np.ones(x.shape[:-1]+(1,))*self.coef0)
                return np.concatenate(parts, axis=-1)
            self.phi = poly2_phi
        
        self.tol = tol
        self.max_iter = max_iter if max_iter>=0 else 10
   
   
    def fit(self, x: np.ndarray, y: np.ndarray, *args, **kwargs):
        self.n = n = len(x)
        self.u = u = np.concatenate((np.ones(n), -np.ones(n)))    
        self.kp = kp = KernelProvider(self.phi, x, u)        
        self.L = L = 2 * n
        self.p = p = np.concatenate((
            self.epsilon * np.ones(n) - y,
            self.epsilon * np.ones(n) + y,
        ), axis=0)
        
        alpha = np.zeros((L,))
        
        #for i in range(n): alpha[i] = alpha[n+i] = np.random.rand()*self.C*1e-2
       
        Q = np.zeros((L,L))
        for i in range(L):
            for j in range(L):
                Q[i,j] = self.kp.Q(i,j)
        
        old_i, old_j = -1, -1
        
        for k in range(self.max_iter):
            print(f"Iteration {k}")
            i_up = self.I_up(alpha)
            i_low = self.I_low(alpha)
    
            tmp_grads = np.array([-self.u[t]*self.grad_f(alpha, t) for t in range(L)])
            m = np.max(tmp_grads[i_up])
            M = np.min(tmp_grads[i_low])

            if m-M<=self.epsilon:                
                # if alpha(k) is a stationary point, stop
                print("Stationary point found")
                break            

            # Otherwise, find a two-element set B={i,j} by WSS
            i,j = self.wss1(alpha, tmp_grads, i_up, i_low, old_i, old_j)
            old_i, old_j = i, j
            B = np.array([i,j])
            print("B=", B)

            # Define N = {1,...,L} \ B
            N = np.array([ix for ix in range(self.L) if ix!=i and ix!=j])
            
            # 2-variable subproblem parameters
            Q = np.array([[self.kp.Q(i,i), self.kp.Q(i,j)],[ self.kp.Q(j,i), self.kp.Q(j,j)]])
            P = p[B] + (self.compute_Q_BN(B,N) @ alpha[N])
            V = np.array([self.u[i], self.u[j]])
            D = - self.u[N] @ alpha[N]
            
            # aij = Kii + Kjj - 2*Kij
            aij = self.kp.K(i,i) + self.kp.K(j,j) - 2*self.kp.K(i,j)
            if aij <= 0:
                print("TOL !!!!!!!!!!!!!!!!")
                fact = (self.tol-aij)/4
                Q += fact * np.eye(2)
                P -= 2*fact*np.array([alpha[i], alpha[j]])
            
            # optimize the subproblem
            ai, aj = self.solve_q2_new(Q,P,V,D, alpha[i], alpha[j], self.u[i], self.u[j])            
            
            print(ai, aj)
            alpha[i], alpha[j] = ai, aj
            
            print("FOUND Aij = ", alpha[i], alpha[j])
            print(f"SOL {k} = ", alpha)


        self.alpha0 = alpha        

        self.w_alpha = np.atleast_1d(self.alpha0[:n]-self.alpha0[n:]) @ self.kp.phi(x)
        
        print("A0=", self.w_alpha)

        self.w_b = np.mean(y - self.phi(x) @ self.w_alpha, axis=0)
        
        """
        grads_0C = [u[i]*self.grad_f(alpha, i) for i in range(L) if 0<alpha[i]<self.C]
        print("LEN GRADS = ", len(grads_0C))
        if len(grads_0C)>0:
            self.w_b = -np.mean(grads_0C)
        else:
            M = np.max([u[i]*self.grad_f(alpha, i) for i in range(L) if (alpha[i]<=0+1e-4 and self.u[i]==-1) or (alpha[i]>=self.C-1e-4 and self.u[i]== 1)])
            m = np.min([u[i]*self.grad_f(alpha, i) for i in range(L) if (alpha[i]<=0+1e-4 and self.u[i]== 1) or (alpha[i]>=self.C-1e-4 and self.u[i]==-1)])
            self.w_b = (M+m)/2
        """
        
        return self
        
    def predict(self, X_set: np.ndarray, *args, **kwargs) -> np.ndarray:
        return self.kp.phi(X_set) @ self.w_alpha + self.w_b
        
    def predict_one(self, X: np.ndarray, *args, **kwargs) -> np.ndarray:
        return (self.kp.phi(X.reshape(1, -1)) @ self.w_alpha + self.w_b)[0]
        
        
    def solve_q2_new(self, Q, P, V, D, aik, ajk, ui, uj):
        """ 
            from V*[ai aj]=D find ai=(D-V[1]*aj)/V[0] and substitute in objective function
            => 2nd degree function with one variable to minimize on a certain interval:
                A*alpha^2 + B*alpha + <ingnored constant term>
            use that V[0], V[1] in {-1, 1} therefore V[0]^2=V[1]^2=1
        """        
        li = (D - V[0]*self.C)/V[1]
        ri = D/V[1]
        if li>ri: li, ri = ri, li
        
        alpha0 = max(0, li)
        alpha1 = min(self.C, ri)
        
        if alpha0>alpha1:             
            raise RuntimeError("No solution?")
        A = Q[0,0] + Q[1,1] - (Q[0,1]+Q[1,0])*V[1]/V[0]
        B = -2*D*V[1] + D*(Q[0,1]+Q[1,0])/V[0] + (P[1]-P[0]*V[1]/V[0])
        
        alphaj = 0
        if abs(A)<1e-4: # linear
            alphaj = alpha0 if B>0 else alpha1
        else:
            alphaj = -B/(2*A)
            if alphaj<alpha0 or alphaj>alpha1 or A<0:
                alphaj = alpha0 if A*alpha0*alpha0+B*alpha0<A*alpha1*alpha1+B*alpha1 else alpha1        
        alphaj += np.clip((2*np.random.rand()-1)*1e-2, 0, self.C)

        alphai = (D-V[1]*alphaj)/V[0]
        return alphai, alphaj        
        
    
    def compute_Q_BN(self, B,N):                
        q = np.zeros((2, self.L-2))
        for x in range(len(B)):
            for y in range(len(N)):
                q[x,y] = self.kp.Q(B[x], N[y])
        return q
        
    def I_up(self, alpha):
        return np.array([i for i in range(len(alpha)) if (alpha[i]<self.C and self.u[i]==1) or (alpha[i]>0 and self.u[i]==-1)])
        
    def I_low(self, alpha):
        return np.array([i for i in range(len(alpha)) if (alpha[i]<self.C and self.u[i]==-1) or (alpha[i]>0 and self.u[i]==1)])
        
    def grad_f(self, alpha, s):
        assert len(alpha) == 2*self.n
        res = 0
        for i in range(self.L):
            res += self.kp.Q(s,i) * alpha[i]
        res += self.p[s]
        return res

    def wss1(self, alpha, tmp_grads, i_up, i_low, old_i, old_j):        
        assert self.p.shape == alpha.shape, f"{self.p.shape} != {alpha.shape}"
        
        L = self.L
        
        i_sorted = i_up[np.argsort(tmp_grads[i_up])[::-1]]
        
        #i = i_up[np.argmax(tmp_grads[i_up])]
        for i in i_sorted:
            a, b = np.zeros(L), np.zeros(L)
            for t in range(L):
                a[t] = self.kp.K(i,i)+self.kp.K(t,t)-2*self.kp.K(i,t)
                if a[t]<=0: a[t] = self.tol
                b[t] = tmp_grads[i] - tmp_grads[t]
            
            values = np.array([-b[t]*b[t]/a[t] for t in i_low if tmp_grads[t]<tmp_grads[i]])
            j = i_low[np.argmin(values)]
            
            if i==j: continue
            
            if (i==old_i and j==old_j): # We are stuck            
                values = np.array([-b[t]*b[t]/a[t] for t in i_low if tmp_grads[t]<tmp_grads[i]])        
                j = np.argmin(values) 
                if j==old_j or j==i:
                    j = np.random.randint(0, L)
                    while i==j:
                        j = np.random.randint(0, L)
            else:
                return i,j
        print("WSS FAILED?????????????????????????????????")
        
        i = i_sorted[0]
        while i==j:
            j = np.random.randint(0, L)
        
        return i,j
        
        
                
                
        