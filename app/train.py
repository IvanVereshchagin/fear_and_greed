import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib


n_samples = 1000  
n_features = 5  
X = np.random.rand(n_samples, n_features)  
y = np.random.randint(0, 101, n_samples)  


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


model_filename = "./app/regression_model.joblib" 
joblib.dump(model, model_filename) 

