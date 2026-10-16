from __future__ import annotations

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .data import DATASETS, dataset_summary, load_dataset
from .ml import experiment, exploration

app = FastAPI(title='Regression Visualization Lab API', version='0.1.0')
origins = [origin.strip() for origin in os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',') if origin.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=['GET', 'POST'], allow_headers=['Content-Type'])

class ExperimentRequest(BaseModel):
    dataset_id: str
    model: str
    train_size: float = Field(ge=.6, le=.9)

def translate_error(error: Exception):
    if isinstance(error, KeyError): raise HTTPException(404, str(error))
    if isinstance(error, (ValueError, FileNotFoundError)): raise HTTPException(422, str(error))
    raise error

@app.get('/api/health')
def health(): return {'status': 'ok'}

@app.get('/api/datasets')
def datasets():
    try: return [dataset_summary(dataset_id) for dataset_id in DATASETS]
    except Exception as error: translate_error(error)

@app.get('/api/datasets/{dataset_id}/exploration')
def get_exploration(dataset_id: str):
    try:
        meta, frame = load_dataset(dataset_id)
        return exploration(frame, meta)
    except Exception as error: translate_error(error)

@app.post('/api/experiments')
def run_experiment(payload: ExperimentRequest):
    try:
        meta, frame = load_dataset(payload.dataset_id)
        return experiment(frame, meta['target'], payload.model, payload.train_size)
    except Exception as error: translate_error(error)
