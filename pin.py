import sys
import json
from argparse import ArgumentParser
from pathlib import Path


CONFIG_PATH = Path.home() / '.pin-config.json'

def main():
    parser = ArgumentParser(
        prog='pin',
        description='Basic shell snippet manager'
    )

    parser.add_argument('snippet', nargs='?', help='Snippet name to use')

    parser.add_argument('-a', '--add', type=str, metavar='COMMAND', help='Add new snippet')
    parser.add_argument('-c', '--change', type=str, metavar='COMMAND', help='change snippet command')
    parser.add_argument('-r', '--remove', action='store_true', help='remove snippet')
    # TODO: extra argument for searching snippets
    parser.add_argument('-l', '--list', action='store_true', help='List all snippets')

    parser.add_argument('--generate-config', action='store_true', help='create default config')
    # TODO: Implement appending different config files
    # parser.add_argument('--append-config', action='store_true', help='Append snippets from home config and current directory config file')

    args = parser.parse_args()

    if args.generate_config:
        create_config()
        return

    config = load_config()

    # Handling flags
    if args.add or args.remove or args.change:
        modify_snippets(config, args)
    elif args.list:
        list_snippets(config)
    
    # Primary action
    # TODO: use shell expressions to evaluate and execute
    snippet = args.snippet

    if snippet:
        if snippet in config:
            print(config[snippet])
        else:
            print(f'Erro: snippet "{snippet}" not found')
    else:
        parser.print_help()

# --- Usages --- exit code 11~19

def modify_snippets(config, args):
    snippet = args.snippet

    if not snippet:
        print('Erro: snippet not specified')
        sys.exit(11)
    
    if args.add:
        if snippet in config:
            print(f'Erro: snippet "{snippet}" already exists')
            sys.exit(11)

        config[snippet] = args.add
    elif args.change:
        if snippet not in config:
            print(f'Erro: snippet "{snippet}" not found')
            sys.exit(11)

        config[snippet] = args.change
    elif args.remove:
        config.pop(snippet, None)

    save_config(config)
    sys.exit(0)


def list_snippets(config):
    # TODO: Implement searching logic if a extra argument is passed
    
    print(f"{'SNIPPET':<15} | {'COMMAND'}")
    for name, command in config.items():
        print(f"{name:<15} | {command}")
    
    sys.exit(0)

# --- JSON manipulation --- exit code 2~9

def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'Erro: config file not found in {CONFIG_PATH.absolute()}')
        sys.exit(2)
    except json.JSONDecodeError:
        print(f'Erro: invalid json config file {CONFIG_PATH.absolute()}.')
        sys.exit(2)


def create_config():
    if CONFIG_PATH.exists():
        print(f'Erro: config file already exists in {CONFIG_PATH.absolute()}')
        sys.exit(3)
    
    default_config = {}
    default_config['hello'] = 'echo "Hello World!"'

    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(default_config, file, indent=2, ensure_ascii=False)

    print(f'Config file created in {CONFIG_PATH.absolute()}')


def save_config(config: dict):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        print(f'Erro: config file not found in {CONFIG_PATH.absolute()}')
        sys.exit(4)
    except json.JSONDecodeError:
        print(f'Erro: invalid json config file {CONFIG_PATH.absolute()}.')
        sys.exit(4)


if __name__ == '__main__':
    main()