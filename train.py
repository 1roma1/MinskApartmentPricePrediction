import os
import numpy as np
import pandas as pd
import joblib

from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

import config
import optimization as opt


def load_data(path, random_state):
    df = pd.read_csv(path)
    features = df.drop("price", axis=1)
    labels = df["price"]

    X_train, X_test, y_train, y_test = \
        train_test_split(features, labels, random_state=random_state)
    return X_train, X_test, y_train, y_test


def get_features(X_train, X_test, features):
    X_train = X_train[features]
    X_test = X_test[features]
    return X_train, X_test


if __name__ == "__main__":
    data_path = os.path.join(config.DATA_PATH, "2023_02_18/cleaned_data.csv")
    X_train, X_test, y_train, y_test = load_data(data_path, config.RANDOM_STATE)

    bin_cols = ['near_the_metro_station']
    cat_cols = ['house_type', 'town_district_name', 'toilet', 'balcony_type']
    num_cols = ["building_year", "area_total", "area_living", "area_kitchen",
                "rooms","storeys", "storey", "ceiling_height"]

    transformer = ColumnTransformer([
        ("bin", OrdinalEncoder(), bin_cols),
        ("cat", OneHotEncoder(), cat_cols),
        ("num", StandardScaler(), num_cols),
    ])

    X_train_tr = transformer.fit_transform(X_train)
    X_test_tr = transformer.transform(X_test)

    model = XGBRegressor()
    
    model.fit(X_train_tr, y_train)
    y_pred = model.predict(X_test_tr)
    print("Test rmse: ", np.sqrt(mean_squared_error(y_test, y_pred)))
    print("Test mae: ", mean_absolute_error(y_test, y_pred))

    model = opt.xgb_optimize(model, X_train_tr, y_train)
    y_pred = model.predict(X_test_tr)
    print("After optimization rmse: ", np.sqrt(mean_squared_error(y_test, y_pred)))
    print("After optimization mae: ", mean_absolute_error(y_test, y_pred))

    predict_pipeline = Pipeline([
            ("preparation", transformer),
            ("est", model),
        ])
    
    joblib.dump(predict_pipeline, "models/minsk_apartment_model.pk")
