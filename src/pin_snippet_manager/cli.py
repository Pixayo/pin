import sys
from argparse import ArgumentParser, Namespace

from .config import CONFIG_PATH
from .jsonIO import create_config
from . import usages


# TODO: Implement appending different config files
# TODO: use shell expressions to evaluate commands

# FIXME: Implement both config.json and snippets.json properly

def main():
    parser = ArgumentParser(
        prog='pin',
        description='Basic shell snippet manager'
    )
    subparser = parser.add_subparsers(dest='action', help='Command to run')

    add = subparser.add_parser('add', help='Add a new snippet')
    add.add_argument('name', 
        help='Snippet name'
    )
    add.add_argument('cmd', nargs='?', default='', 
        help='Command to pin surrounded by quotation marks'
    )
    add.set_defaults(func=usages.add_snippet)

    remove = subparser.add_parser('rm', help='Remove a snippet')
    remove.add_argument('name', 
        help='Snippet name'
    )
    remove.set_defaults(func=usages.remove_snippet)

    show = subparser.add_parser('show', help='Show all snippets')
    show.add_argument('name', nargs='?', 
        help='Optionally search for a snippet'
    )
    show.set_defaults(func=usages.list_snippets)

    args = parser.parse_args()

    try:
        if args.action == 'init':
            create_config(CONFIG_PATH)
            print(f'config created in: {CONFIG_PATH}', file=sys.stderr)
            return 0
        

        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help(file=sys.stderr)

    except (ValueError, FileNotFoundError) as err:
        print(err, file=sys.stderr)
        return 1
