from pathlib import Path
from platformdirs import user_config_dir


CONFIG_DIR: Path = Path(user_config_dir('pin'))
CONFIG_PATH: Path = CONFIG_DIR / 'config.json'

DEFAULT_CONFIG: dict = {
    "hello": "'Hello World!'"
}