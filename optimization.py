import numpy as np

from sklearn.model_selection import GridSearchCV


def xgb_optimize(model, X, y, params=None):
    if params is None:
        params = {
            'n_estimators': np.arange(20, 40, 5),
            'max_depth': np.arange(3, 9, 2),
            'learning_rate': np.arange(0.05, 0.2, 0.05),
        }
    xgb_grid_search = GridSearchCV(model, params, scoring="neg_mean_squared_error", cv=5, n_jobs=-1)
    xgb_grid_search.fit(X, y)
    return xgb_grid_search