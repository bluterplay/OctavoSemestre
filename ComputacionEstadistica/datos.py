import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def sample_beta_0(y, x, beta_1, tau, mu_0, tau_0):
    N = len(y)
    assert len(x) == N
    precision = tau_0 + tau * N
    mean = tau_0 * mu_0 + tau * np.sum(y - beta_1 * x)
    mean /= precision
    return np.random.normal(mean, 1 / np.sqrt(precision))

def sample_beta_1(y, x, beta_0, tau, mu_1, tau_1):
    N = len(y)
    assert len(x) == N
    precision = tau_1 + tau * np.sum(x * x)
    mean = tau_1 * mu_1 + tau * np.sum( (y - beta_0) * x)
    mean /= precision
    #print(f" Beta 1 mean= {mean}, precision={precision}")
    return np.random.normal(mean, 1 / np.sqrt(precision))

def sample_tau(y, x, beta_0, beta_1, alpha, beta):
    N = len(y)
    alpha_new = alpha + N / 2
    resid = y - beta_0 - beta_1 * x
    beta_new = beta + np.sum(resid * resid) / 2
    #print(f"error= {resid}, alpha={alpha_new}, beta={beta_new}")
    return np.random.gamma(alpha_new, 1 / beta_new)

## specify initial values
init = {"beta_0": 0,
        "beta_1": 0,
        "tau": 2}

## specify hyper parameters
hypers = {"mu_0": 0,
         "tau_0": 1,
         "mu_1": 0,
         "tau_1": 1,
         "alpha": 2,
         "beta": 1}



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

def gibbs(y, x,X, iters,coeficients,regres,init, hypers):
    assert len(y) == len(x)
    beta_0 = init["beta_0"]
    beta_1 = init["beta_1"]
    tau = init["tau"]
    
    trace = np.zeros((iters, 3)) ## trace to store values of beta_0, beta_1, tau
    for it in range(iters):
        regres.sampleIntercept(X,y)
        for var in coeficients:
            regres.sampleCoeficients(X,y,var)
        regres.sampleTau(X,y)
        beta_0 = sample_beta_0(y, x, beta_1, tau, hypers["mu_0"], hypers["tau_0"])
        beta_1 = sample_beta_1(y, x, beta_0, tau, hypers["mu_1"], hypers["tau_1"])
        tau = sample_tau(y, x, beta_0, beta_1, hypers["alpha"], hypers["beta"])
        trace[it,:] = np.array((beta_0, beta_1, tau))

regres= BayesianLinearRegression(n_params=2,alpha=2,beta=1, tau=2)
coeficients=[key for key in  regres.dc_coeficients.keys()]
coeficients.remove("Beta_0")
coeficients.remove("Tau")
X= x.reshape(-1,1)

gibbs(y,x,X, 10000, coeficients, regres, init,hypers)