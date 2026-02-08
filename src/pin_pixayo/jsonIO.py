import json
from pathlib import Path

from .config import DEFAULT_CONFIG


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f'config file not found in {path.absolute()}')

    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f'could not load JSON file {path.absolute()}: \n{e.msg}') from e


def create_config(path: Path):
    if path.exists():
        raise ValueError(f'config file already exists in {path.absolute()}')

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(DEFAULT_CONFIG, file, indent=2, ensure_ascii=False)


def save_config(path: Path, config: dict):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=2, ensure_ascii=False)

