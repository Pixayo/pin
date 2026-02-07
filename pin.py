import sys
import json
from argparse import ArgumentParser, Namespace
from pathlib import Path


CONFIG_PATH = Path('./config.json')

def main():
    parser = ArgumentParser(
        prog='pin',
        description='basic shell snippet manager build with Python'
    )

    parser.add_argument('snippet', nargs='?', help='predefined snippet to use')

    parser.add_argument('-a', '--add', type=str, metavar='COMMAND', help='add new snippet and pin a command to it')
    # parser.add_argument('-r', help='remove snippet or category', action='store_true')
    # parser.add_argument('-c', help='change snippet expression')
    # parser.add_argument('-s' help='show every snippet under a category', action='store_true')

    parser.add_argument('--generate-config', help='create a default config json', action='store_true')
    # parser.add_argument('--dump-config', help='dump snippets from one json file to the current config file')

    args: Namespace = parser.parse_args()

    if args.generate_config:
        create_config()
        return

    config: dict = load_config()

    # Handling flags
    if args.add:
        add_snippet(config, args.add, args.snippet)
    

    print(config[args.snippet])


# --- Usages ---

def add_snippet(config: dict, command: str, snippet: str):
    if not snippet:
        print('Erro: snippet not specified')
        print('Usage: pin -a [COMMAND] [SNIPPET]')
        sys.exit(11)
    
    if snippet in config:
        print(f'Erro: snippet {snippet} already exists')
        sys.exit(11)
    
    config[snippet] = command

    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=2, ensure_ascii=True)


# --- JSON manipulation ---

def create_config():
    if CONFIG_PATH.exists():
        print(f'Erro: config file already exists in {CONFIG_PATH.absolute()}')
        sys.exit(2)
    
    default_config = {}
    default_config['auto-generated'] = 'echo you-can-remove-me'

    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(default_config, file, indent=2, ensure_ascii=True)

    print(f'Config file created in {CONFIG_PATH.absolute()}')


def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Erro: config file not found in {CONFIG_PATH.absolute()}')
        sys.exit(3)
    except json.JSONDecodeError:
        print(f'Erro: invalid json config file {CONFIG_PATH.absolute()}.')
        sys.exit(3)


main()