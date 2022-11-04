import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier as rf
import sklearn
import joblib

df = pd.read_csv('data/student-mat.csv', sep=';')

#definition of Qual student
#df['qual_student'] = np.where(df['G3']>=15, 1, 0) 

#include = ['school','reason','failures','activities','higher','absences','G1','G2','qual_student']
include = ['school','reason','failures','activities','higher','absences','G1','G2','G3']
df.drop(columns=df.columns.difference(include), inplace = True) #8 variables

categoricals = []
for col, col_type in df.dtypes.iteritems():
     if col_type == 'O': #strings are categorical
        if col.isnumeric():  #if it is a number in a string form, get it back to a number
            pd.to_numeric(col)
        else:
            categoricals.append(col)
    
df_conv = pd.get_dummies(df, columns=categoricals)

print(df_conv)
     
#dependent_variable = 'qual_student'
dependent_variable = 'G3'
x = df_conv[df_conv.columns.difference([dependent_variable])]
y = df_conv[dependent_variable]
clf = rf(n_estimators = 1000)
clf.fit(x, y)



pred = clf.predict(x)
accuracy = sklearn.metrics.f1_score(y, pred, average='weighted')
print("Accuracy:" + str(accuracy))

joblib.dump(clf, 'app/handlers/model.pkl')

