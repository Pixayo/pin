from pathlib import Path


# TODO: Break down pin-config.json into config.json and snippets.json

CONFIG_PATH = Path.home() / '.pin-config.json'

DEFAULT_CONFIG = {
    'hello': 'echo "Hello World!"'
}