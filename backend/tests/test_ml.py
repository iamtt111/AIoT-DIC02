import pandas as pd
from app.data import load_dataset
from app.ml import experiment

def test_experiment_returns_metrics_and_predictions():
    frame = pd.DataFrame({'spend': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'state': ['A', 'B'] * 5, 'Profit': [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]})
    outcome = experiment(frame, 'Profit', 'linear_regression', .7)
    assert {'r2', 'rmse', 'mae'} == set(outcome['metrics'])
    assert len(outcome['predictions']['actual']) == 3
    assert outcome['feature_importance']['values']

def test_real_datasets_support_all_models():
    for dataset_id in ('startups', 'boston'):
        meta, frame = load_dataset(dataset_id)
        assert len(frame) > 40
        for model in ('linear_regression', 'decision_tree', 'random_forest'):
            outcome = experiment(frame, meta['target'], model, .8)
            assert len(outcome['predictions']['actual']) > 0
            assert outcome['metrics']['rmse'] >= 0
