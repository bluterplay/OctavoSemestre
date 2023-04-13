import pandas as pd
from pickle import load
class pipeline():

    def __init__(self,df):
        self.df= df.copy()
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
        for dis in self.ls_dis:
            file= 'ModelsEnc/Label_' + dis +'.sav'
            le= load(open(file, 'rb'))
            self.df[dis]=le.transform(self.df[dis])
        self.df[self.ls_cont]=self.df[self.ls_cont].fillna(self.df[self.ls_cont].median())
        print(self.df)

    def scaling(self):
        scx= load(open('ModelsEnc/Scaler.sav', 'rb'))
        X= self.df[self.ls_cont+self.ls_dis]
        y= self.df[self.target]
        X= scx.transform(X)
        return X,y
    

data=pd.read_csv("Data/churn.csv")
test= pipeline(data)
test.convertFloat()
test.imputer()
X,y=test.scaling()
print(X,y)