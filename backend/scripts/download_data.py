from pathlib import Path
from urllib.request import urlretrieve

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
DATA_DIR.mkdir(exist_ok=True)
SOURCES = {
    '50_Startups.csv': 'https://raw.githubusercontent.com/SantiagoMorenoV/50-Startups-Multiple-Reg/main/50_Startups.csv',
    'BostonHousing.csv': 'https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv',
}

for filename, url in SOURCES.items():
    target = DATA_DIR / filename
    print(f'Downloading {filename}…')
    urlretrieve(url, target)
print('Datasets are ready.')
