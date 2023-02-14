import os
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

import config
import optimization as opt


def load_data(path, random_state):
    df = pd.read_csv(path)
    features = df.drop("target_price", axis=1)
    labels = df["target_price"]

    X_train, X_test, y_train, y_test = \
        train_test_split(features, labels, random_state=random_state)
    return X_train, X_test, y_train, y_test


def get_features(X_train, X_test, features):
    X_train = X_train[features]
    X_test = X_test[features]
    return X_train, X_test


if __name__ == "__main__":
    data_path = os.path.join(config.DATA_PATH, "22_12_2022_cleaned_data.csv")
    X_train, X_test, y_train, y_test = load_data(data_path, config.RANDOM_STATE)
    X_train, X_test = get_features(X_train, X_test, ["total_area"])

    transformer = ColumnTransformer([
        ("num", StandardScaler(), ["total_area"]),
    ])

    X_train_tr = transformer.fit_transform(X_train)
    X_test_tr = transformer.transform(X_test)

    model = XGBRegressor()
    
    model.fit(X_train_tr, y_train)
    y_pred = model.predict(X_test_tr)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("Test rmse: ", rmse)

    model = opt.xgb_optimize(model, X_train_tr, y_train)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print("After optimization rmse: ", rmse)

    predict_pipeline = Pipeline([
            ("preparation", transformer),
            ("est", model),
        ])
    
    joblib.dump(predict_pipeline, "models/minsk_apartment_model.pk")
