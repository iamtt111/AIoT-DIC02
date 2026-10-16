from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

RANDOM_STATE = 42
MODELS = {
    'linear_regression': ('線性迴歸', LinearRegression()),
    'decision_tree': ('決策樹迴歸', DecisionTreeRegressor(random_state=RANDOM_STATE, max_depth=5)),
    'random_forest': ('隨機森林迴歸', RandomForestRegressor(random_state=RANDOM_STATE, n_estimators=180, min_samples_leaf=2, n_jobs=-1)),
}

def build_pipeline(frame: pd.DataFrame, target: str, model_key: str) -> tuple[Pipeline, list[str]]:
    if model_key not in MODELS: raise ValueError('不支援的模型。')
    features = [column for column in frame.columns if column != target]
    numeric = frame[features].select_dtypes(include='number').columns.tolist()
    categorical = [column for column in features if column not in numeric]
    numeric_steps = [('imputer', SimpleImputer(strategy='median'))]
    if model_key == 'linear_regression': numeric_steps.append(('scaler', StandardScaler()))
    preprocess = ColumnTransformer([
        ('numeric', Pipeline(numeric_steps), numeric),
        ('categorical', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical),
    ], remainder='drop')
    return Pipeline([('preprocess', preprocess), ('model', MODELS[model_key][1])]), features

def experiment(frame: pd.DataFrame, target: str, model_key: str, train_size: float) -> dict:
    pipeline, features = build_pipeline(frame, target, model_key)
    x_train, x_test, y_train, y_test = train_test_split(frame[features], frame[target], train_size=train_size, random_state=RANDOM_STATE)
    pipeline.fit(x_train, y_train)
    predicted = pipeline.predict(x_test)
    model = pipeline.named_steps['model']
    output_names = pipeline.named_steps['preprocess'].get_feature_names_out()
    if hasattr(model, 'feature_importances_'):
        scores, label = model.feature_importances_, '特徵重要性'
    else:
        scores, label = np.abs(model.coef_), '標準化係數絕對值'
    top = sorted(zip(output_names, scores), key=lambda item: item[1], reverse=True)[:10]
    actual = y_test.to_numpy(dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    line = [float(min(actual.min(), predicted.min())), float(max(actual.max(), predicted.max()))]
    return {
        'model_label': MODELS[model_key][0],
        'metrics': {'r2': float(r2_score(y_test, predicted)), 'rmse': float(np.sqrt(mean_squared_error(y_test, predicted))), 'mae': float(mean_absolute_error(y_test, predicted))},
        'predictions': {'actual': actual.tolist(), 'predicted': predicted.tolist(), 'line': line},
        'residuals': (actual - predicted).tolist(),
        'feature_importance': {'label': label, 'names': [name.replace('numeric__', '').replace('categorical__', '') for name, _ in top], 'values': [float(value) for _, value in top]},
    }

def exploration(frame: pd.DataFrame, meta: dict) -> dict:
    target = meta['target']
    numeric = frame.select_dtypes(include='number')
    correlations = numeric.corr().round(3)
    related = correlations[target].drop(target).abs().sort_values(ascending=False)
    feature = related.index[0]
    return {**meta, 'record_count': len(frame), 'feature_count': len(frame.columns) - 1,
        'target_distribution': {'values': frame[target].astype(float).tolist()},
        'relationship': {'feature': feature, 'x': frame[feature].astype(float).tolist(), 'y': frame[target].astype(float).tolist()},
        'correlation': {'columns': correlations.columns.tolist(), 'matrix': correlations.values.tolist()}}
