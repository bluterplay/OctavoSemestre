import numpy as np
import sys 

sys.setrecursionlimit(1000)

class GLC():
    def __init__(self,A=7**5,C=0,M=2**31 -1,seed=1234):
        self.A= A
        self.C= C
        self.M= M
        self.seed= seed
        self.ls_num= []
    
    def operation(self,x):
        sn= (self.A*x + self.C) %self.M
        self.ls_num.append(x/self.M)
        return sn

    def generate(self,samples):
        if(samples==0):
            return self.seed
        else:
            samples-=1
            return self.operation(self.generate(samples))

generador= GLC()
ls=generador.generate(10) 
for i in generador.ls_num:
    print(i)