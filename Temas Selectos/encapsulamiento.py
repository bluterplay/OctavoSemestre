import pandas as pd
from pickle import load
from numpy.random import rand
class pipeline():

    def __init__(self,df, threshold):
        self.df= df.copy()
        self.threshold= threshold
        self.target= 'Churn'
        self.ls_cont=['tenure', 'MonthlyCharges', 'TotalCharges']
        self.ls_dis= [x for x in self.df.columns[1:] if x not in self.ls_cont+ [self.target]]
        self.ls_dis.remove("PhoneService")
        self.df['Churn'] = self.df['Churn'].map({'Yes': 1, 'No': 0})

    def convertFloat(self):
        ls_fail= []
        for index, row in self.df.iterrows():
            total= row["TotalCharges"]
            tenure= row["tenure"]
            mes= row['MonthlyCharges']
            try:
                float(total)
                float(tenure)
                float(mes)
            except :
                ls_fail.append(index)
        self.df.drop(ls_fail, inplace=True)

        for cont in self.ls_cont:
            self.df[cont]= self.df[cont].apply(lambda x: float(x))

    def imputer(self):
        self.df[self.ls_cont]=self.df[self.ls_cont].fillna(self.df[self.ls_cont].median())
        for dis in self.ls_dis:
            file= 'ModelsEnc/Label_' + dis +'.sav'
            le= load(open(file, 'rb'))
            self.df[dis]=le.transform(self.df[dis])
        self.df[self.ls_cont]=self.df[self.ls_cont].fillna(self.df[self.ls_cont].median())


    def scaling(self):
        scx= load(open('ModelsEnc/Scaler.sav', 'rb'))
        X= self.df[self.ls_cont+self.ls_dis]
        y= self.df[self.target]
        X= scx.transform(X)
        return X,y
    
    def selectModel(self):
        U= rand()
        if(U<=self.threshold):
            clf= load(open('ModelsEnc/champion.sav', 'rb'))
        else:
            clf= load(open('ModelsEnc/challenger.sav', 'rb'))
        return clf

    def predict(self,X,y, clf):
        y_pred= clf.predict(X)
        self.df["y_hat"]= y_pred
        return y_pred
    

data=pd.read_csv("Data/churn.csv")
test= pipeline(data,.5)
test.convertFloat()
test.imputer()
X,y=test.scaling()
clf= test.selectModel()
y_pred= test.predict(X,y,clf)
print(test.df[[test.target,"y_hat"]])
