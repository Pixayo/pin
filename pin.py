import sys
import json
from argparse import ArgumentParser, Namespace
from pathlib import Path


# FIXME: Make config file path global
CONFIG_PATH = Path('./config.json')

def main():
    parser = ArgumentParser(
        prog='pin',
        description='Basic shell snippet manager'
    )

    parser.add_argument('snippet', nargs='?', help='Snippet name to use')

    parser.add_argument('-a', '--add', type=str, metavar='COMMAND', help='Add new snippet')
    parser.add_argument('-l', '--list', action='store_true', help='List all snippets')
    # parser.add_argument('-r', help='remove snippet or category', action='store_true')
    # parser.add_argument('-c', help='change snippet expression')

    parser.add_argument('--generate-config', action='store_true', help='create default config')

    args = parser.parse_args()

    if args.generate_config:
        create_config()
        return

    config: dict = load_config()

    # Handling flags
    if args.add:
        add_snippet(config, args.add, args.snippet)
    elif args.list:
        list_snippets(config)
    
    if args.snippet:
        if args.snippet in config:
            print(config[args.snippet])
        else:
            print(f'Erro: snippet {snippet} not found')
    else:
        parser.print_help()

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

    sys.exit(0)


def list_snippets(config):
    print(f"{'SNIPPET':<15} | {'COMMAND'}")
    print("-" * 30)
    for name, command in config.items():
        print(f"{name:<15} | {command}")
    
    sys.exit(0)

# --- JSON manipulation ---

def create_config():
    if CONFIG_PATH.exists():
        print(f'Erro: config file already exists in {CONFIG_PATH.absolute()}')
        sys.exit(2)
    
    default_config = {}
    default_config['hello'] = 'echo "Hello World!"'

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


if __name__ == '__main__':
    main()