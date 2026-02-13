import json
from pathlib import Path


DEFAULT_CONFIG: dict = {
    "hello": "echo 'Hello World!'"
}

def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f'config file not found in {path.absolute()}')

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as err:
        raise ValueError(f'could not load JSON file {path.absolute()}: \n{err.msg}') from err


def save_config(path: Path, config: dict):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=2, ensure_ascii=False)


def create_config(path: Path):
    if path.exists():
        raise ValueError(f'config file already exists in {path.absolute()}')
    
    save_config(path, DEFAULT_CONFIG)
