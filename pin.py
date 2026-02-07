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

    # TODO: extra argument for "--list", searching snippets by reference
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', type=str, metavar='COMMAND', help='Add new snippet')
    group.add_argument('-c', '--change', type=str, metavar='COMMAND', help='change snippet command')
    group.add_argument('-r', '--remove', action='store_true', help='remove snippet')
    group.add_argument('-l', '--list', action='store_true', help='List all snippets')

    group.add_argument('--create-config', action='store_true', help='create default config')
    # TODO: Implement appending different config files
    # group.add_argument('--append-config', action='store_true', help='Append snippets from home config and current directory config file')

    # Main argument
    parser.add_argument('snippet', nargs='?', help='Snippet name to use')

    args = parser.parse_args()

    # TODO: use shell expressions to evaluate and execute
    try:
        if args.create_config:
            create_config(CONFIG_PATH)
            return

        config = load_config(CONFIG_PATH)

        if args.add or args.remove or args.change:
            modify_snippets(config, args)
        elif args.list:
            list_snippets(config)
        elif args.snippet:
            if args.snippet in config:
                print(config[args.snippet])
            else:
                print(f'snippet "{args.snippet}" not found')
        else:
            parser.print_help()
    except (ValueError, FileNotFoundError) as e:
        print(e)
        sys.exit(1)


# --- Usages ---

def modify_snippets(config, args):
    snippet = args.snippet

    if not snippet:
        raise ValueError('snippet not specified')
    
    if snippet in config and args.add:
        raise ValueError(f'snippet "{snippet}" already exists')
    elif snippet not in config and (args.remove or args.change):
        raise ValueError(f'snippet "{snippet}" does not exist')

    if args.add:
        config[snippet] = args.add
    elif args.change:
        config[snippet] = args.change
    elif args.remove:
        config.pop(snippet, None)

    save_config(CONFIG_PATH, config)


def list_snippets(config):
    # TODO: Implement searching logic if a extra argument is passed
    
    print(f"{'SNIPPET':<15} | {'COMMAND'}")
    for name, command in config.items():
        print(f"{name:<15} | {command}")

# --- JSON manipulation --- 

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
        print(f'Erro: config file already exists in {path.absolute()}')
        sys.exit(3)
    
    default_config = {}
    default_config['hello'] = 'echo "Hello World!"'

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(default_config, file, indent=2, ensure_ascii=False)

    print(f'Config file created in {path.absolute()}')


def save_config(path: Path, config: dict):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
    except json.JSONDecodeError as e:
        raise ValueError(f'could not save JSON file {path.absolute()}: \n{e.msg}') from e


if __name__ == '__main__':
    main()