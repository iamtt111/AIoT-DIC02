from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dataset_and_experiment_endpoints():
    datasets = client.get('/api/datasets')
    assert datasets.status_code == 200
    assert {item['id'] for item in datasets.json()} == {'startups', 'boston'}
    for dataset_id in ('startups', 'boston'):
        exploration = client.get(f'/api/datasets/{dataset_id}/exploration')
        assert exploration.status_code == 200
        assert exploration.json()['target_distribution']['values']
    experiment = client.post('/api/experiments', json={'dataset_id': 'boston', 'model': 'random_forest', 'train_size': .8})
    assert experiment.status_code == 200
    assert 'metrics' in experiment.json()

def test_health_endpoint():
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
