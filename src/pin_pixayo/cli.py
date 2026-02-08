from argparse import ArgumentParser, Namespace

from .config import *
from .jsonIO import *
from .usages import *


# TODO: Implement appending different config files
# TODO: use shell expressions to evaluate commands

# FIXME: Implement both config.json and snippets.json properly

def main():
    parser = ArgumentParser(
        prog='pin',
        description='Basic shell snippet manager'
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', type=str, metavar='COMMAND', help='Add new snippet')
    group.add_argument('-c', '--change', type=str, metavar='COMMAND', help='Change snippet command')
    group.add_argument('-r', '--remove', action='store_true', help='Remove snippet')
    group.add_argument('-l', '--list', action='store_true', help='List all snippets')

    group.add_argument('--create-config', action='store_true', help='Create default config')
    # group.add_argument('--append-config', action='store_true', help='Append snippets from home config and current directory config file')

    # Main argument
    parser.add_argument('snippet', nargs='?', help='Snippet name to use')

    args: Namespace = parser.parse_args()

    try:
        if args.create_config:
            create_config(CONFIG_PATH)
            print(f'config created in: {CONFIG_PATH}')
            return 0

        config: dict = load_config(CONFIG_PATH)

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
        return 1
