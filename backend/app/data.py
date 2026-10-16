from __future__ import annotations

from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'

DATASETS = {
    'startups': {
        'name': '50 Startups', 'file': '50_Startups.csv', 'target': 'Profit',
        'description': '以研發、行政、行銷支出與州別預測新創公司的獲利。',
        'source': 'Kaggle 50 Startups dataset (public teaching mirror)',
    },
    'boston': {
        'name': 'Boston Housing', 'file': 'BostonHousing.csv', 'target': 'MEDV',
        'description': '以住宅與環境特徵預測房價中位數；僅供探索迴歸模型。',
        'source': 'Boston Housing / UCI Machine Learning Repository',
    },
}

def _normalise_columns(frame: pd.DataFrame, dataset_id: str) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = [str(col).strip() for col in frame.columns]
    if dataset_id == 'startups':
        aliases = {'R&D Spend': 'R&D Spend', 'R&DSpend': 'R&D Spend', 'Marketing Spend': 'Marketing Spend'}
        frame = frame.rename(columns=aliases)
    else:
        frame.columns = [col.upper() for col in frame.columns]
        if 'MEDV' not in frame and 'MEDV ' in frame: frame = frame.rename(columns={'MEDV ': 'MEDV'})
    return frame

def load_dataset(dataset_id: str) -> tuple[dict, pd.DataFrame]:
    if dataset_id not in DATASETS:
        raise KeyError('不支援的資料集。')
    meta = DATASETS[dataset_id]
    path = DATA_DIR / meta['file']
    if not path.exists():
        raise FileNotFoundError('資料檔尚未下載。請在 backend 執行 python scripts/download_data.py。')
    return meta, _normalise_columns(pd.read_csv(path), dataset_id).dropna()

def dataset_summary(dataset_id: str) -> dict:
    meta, frame = load_dataset(dataset_id)
    return {**meta, 'id': dataset_id, 'record_count': len(frame), 'feature_count': len(frame.columns) - 1, 'columns': list(frame.columns)}
