import json
from pathlib import Path

from .config import DEFAULT_CONFIG


def load_config(path: Path) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(f'file not found: {path.absolute()}')

    except json.JSONDecodeError as err:
        msg = f'invalid JSON format in {path.absolute()}'
        raise ValueError(f'{msg} \n{err.msg} at line: {err.lineno}') from err


def save_config(path: Path, config: dict):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=2, ensure_ascii=False)


def create_config(path: Path):
    if path.exists():
        raise FileExistsError(f'config file already exists in {path.absolute()}')
    
    save_config(path, DEFAULT_CONFIG)
