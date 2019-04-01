
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

path = 'football.csv'
original_data = pd.read_csv(path, sep=';' , decimal=',')
#Initializations
y = original_data.loc[:,'cluster']  
x = original_data.loc[:,'C1':'Y11']
split  = np.rint(0.8*x.shape[0])
X_clean_train = x[:int(split)].values
X_clean_val = x[int(split):].values
y_train = y[:int(split)]
y_val = y[int(split):]

#Clasification model
logreg = LogisticRegression(solver='lbfgs')
logreg.fit(X_clean_train, y_train)

#Function used to predict the output
logreg.predict([X_clean_train[2]])[0]






