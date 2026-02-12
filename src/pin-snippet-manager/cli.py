import sys
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
    subparser = parser.add_subparsers(dest='command', help='Command to run')

    add = subparser.add_parser('add', help='Add a new snippet')
    add.add_argument('name', help='Snippet name')
    add.add_argument('cmd', nargs='?', default='', help='Command to pin')

    rm = subparser.add_parser('rm', help='Remove a snippet')
    rm.add_argument('name', help='Snippet name')

    show = subparser.add_parser('show', help='Show all snippets')
    show.add_argument('name', nargs='?', help='Optionally search for a snippet')

    args = parser.parse_args()

    try:
        if args.command == 'init':
            create_config(CONFIG_PATH)
            print(f'config created in: {CONFIG_PATH}', file=sys.stderr)
            return 0

        config = load_config(CONFIG_PATH)

        if args.command == 'add':
            pass
            # ...

        elif args.command == 'rm':
            pass
            #...
        
        elif args.command == 'show':
            pass
            # ...

        # elif args.command == 'append':
        #     pass
        #     # ...

        elif args.snippet:
            if args.snippet in config:
                print(config[args.snippet])
            else:
                print(f'snippet "{args.snippet}" not found')

        else:
            parser.print_help()

    except (ValueError, FileNotFoundError) as err:
        print(err, file=sys.stderr)
        return 1
