from pathlib import Path
from platformdirs import user_config_dir


# TODO: implement save/load settings like: paths, constants and defaults
#       from a JSON file

CONFIG_DIR: Path = Path(user_config_dir('pin'))
CONFIG_PATH: Path = CONFIG_DIR / 'config.json'