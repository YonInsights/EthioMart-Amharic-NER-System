from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV    
import pandas as pd
import joblib

def train_model(df, target='views'):
    """Train predictive model"""
    X = df.drop(columns=[target, 'id', 'date', 'message'])
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    print(f"RMSE: {mean_squared_error(y_test, preds, squared=False)}")
    print(f"R²: {r2_score(y_test, preds)}")
    
    return model, X.columns.tolist()
def tune_hyperparameters(X_train, y_train):
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    
    grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=3)
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_