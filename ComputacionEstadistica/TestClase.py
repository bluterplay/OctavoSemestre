import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




class BayesianLinearRegression():
    
    def __init__(self,n_params,alpha,beta, tau):
        self.n_params= n_params
        self.dc_coeficients= {"Beta_"+str(i):[0] for i in range(n_params) }
        self.dc_mus= {"Beta_"+str(i):0 for i in range(n_params) }
        self.dc_taus= {"Beta_"+str(i):1 for i in range(n_params) }
        self.dc_columns={"Beta_"+str(i):i-1 for i in range(n_params) }
        self.ls_alpha=[alpha]
        self.ls_beta= [beta]
        self.dc_coeficients["Tau"]= [tau]
        
    def sampleIntercept(self, x,y):
        N = len(y)
        assert len(x) == N
        precision = self.dc_taus["Beta_0"] + self.dc_coeficients["Tau"][-1] * N
        error=y
        ls= [key for key in  self.dc_coeficients.keys()]
        ls.remove("Beta_0")
        ls.remove("Tau")
        for coeficient in ls:
            error -=  self.dc_coeficients[coeficient][-1] * x[:,self.dc_columns[coeficient]]
        mean= self.dc_taus["Beta_0"]* self.dc_mus["Beta_0"] + self.dc_coeficients["Tau"][-1]*np.sum(error)
        mean /= precision
    
        
        self.dc_coeficients["Beta_0"].append(np.random.normal(mean, 1 / np.sqrt(precision)))
    
    def sampleCoeficients(self,x,y,var):
        N = len(y)
        assert len(x) == N
        error=(y- self.dc_coeficients["Beta_0"][-1])
        precision = self.dc_taus[var] + self.dc_coeficients["Tau"][-1] * np.sum(x[:,self.dc_columns[var]] * x[:,self.dc_columns[var]])
        ls= [key for key in  self.dc_coeficients.keys()]
        ls.remove(var)
        ls.remove("Tau")
        ls.remove("Beta_0")
        for coeficient in ls:
            error -=  self.dc_coeficients[coeficient][-1] * x[:,self.dc_columns[coeficient]]
        mean= self.dc_taus[var]* self.dc_mus[var] + self.dc_coeficients["Tau"][-1]*np.sum(error*x[:,self.dc_columns[var]])
        mean /= precision
        self.dc_coeficients[var].append(np.random.normal(mean, 1 / np.sqrt(precision)))
        
    def sampleTau(self,x,y):
        N = len(y)
        self.ls_alpha.append(self.ls_alpha[0] + N / 2)
        error= y- self.dc_coeficients["Beta_0"][-1]
        ls= [key for key in  self.dc_coeficients.keys()]
        ls.remove("Beta_0")
        ls.remove("Tau")
        for coeficient in ls:
            error-= self.dc_coeficients[coeficient][-1]* x[:,self.dc_columns[coeficient]]
        
        self.ls_beta.append(self.ls_beta[0] + np.sum(error*error)/2)
        self.dc_coeficients["Tau"].append(np.random.gamma(self.ls_alpha[-1], 1/self.ls_beta[-1]))


np.random.seed(0)
beta_0_true = -2
beta_1_true = 12
tau_true = 2

N = 50
x = np.random.uniform(low = 0, high = 4, size = N)
y = np.random.normal(beta_0_true + beta_1_true * x, 1 / np.sqrt(tau_true))

def gibbs(y, x, iters,coeficients,regres):
    assert len(y) == len(x)
    for it in range(iters):
        regres.sampleIntercept(x,y)
        for var in coeficients:
            regres.sampleCoeficients(x,y,var)
        regres.sampleTau(x,y)

regres= BayesianLinearRegression(n_params=2,alpha=2,beta=1, tau=2)
coeficients=[key for key in  regres.dc_coeficients.keys()]
coeficients.remove("Beta_0")
coeficients.remove("Tau")
X= x.reshape(-1,1)

gibbs(y,X, 10000, coeficients, regres)