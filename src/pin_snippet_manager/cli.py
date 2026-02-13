import sys
from argparse import ArgumentParser, Namespace

from .config import CONFIG_PATH
from .jsonIO import create_config
from . import usages


# TODO: use shell expressions to evaluate commands
# TODO: 

def main():
    parser = ArgumentParser(
        prog='pin',
        description='Basic shell snippet manager',
    )
    subparser = parser.add_subparsers(dest='action', help='Command to run')

    # ADD subcommand
    add = subparser.add_parser('add', help='Add a new snippet')
    add.add_argument('name', 
        help='Snippet name'
    )
    add.add_argument('cmd', nargs='?', default='', 
        help='Command to pin surrounded by quotation marks'
    )
    add.set_defaults(func=usages.add_snippet)

    # REMOVE subcommand
    remove = subparser.add_parser('rm', help='Remove a snippet')
    remove.add_argument('name', 
        help='Snippet name'
    )
    remove.set_defaults(func=usages.remove_snippet)

    # SHOW subcommand
    show = subparser.add_parser('show', help='Show all snippets')
    show.add_argument('name', nargs='?', 
        help='Optionally search for a snippet'
    )
    show.set_defaults(func=usages.show_snippets)

    # INIT subcommand
    init = subparser.add_parser('init', help='Initialize Pin default setup')
    init.set_defaults(func=usages.initialize)

    # TODO: EXEC subcommand, for execution snippets as a subprocess

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
