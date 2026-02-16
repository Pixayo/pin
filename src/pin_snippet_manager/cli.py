import sys
from argparse import ArgumentParser, Namespace

from .config import CONFIG_PATH
from .jsonIO import load_config
from . import usages


# TODO: better error handling
# TODO: shell integration

def main():
    parser = get_parser()
    args = parser.parse_args()

    try:
        if not hasattr(args, 'func'):
            parser.print_help(file=sys.stderr)
            return 0
        
        if args.func == usages.initialize:
            args.func()
        else:
            config = load_config(CONFIG_PATH)
            args.func(args, config)

    except (ValueError, KeyError, FileNotFoundError, FileExistsError) as err:
        print(err, file=sys.stderr)
        return 1


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='pin',
        description='Shell snippet manager',
    )
    subparser = parser.add_subparsers(dest='action', help='Command to run')

    use = subparser.add_parser('use', help='Snippet to use')
    use.add_argument('name', help='Snippet name')
    use.set_defaults(func=usages.print_snippet)

    add = subparser.add_parser('add', help='Add a snippet')
    add.add_argument('name', help='Snippet name')
    add.add_argument('cmd', nargs='?', default='', help='Command surrounded by quotation marks')
    add.set_defaults(func=usages.add_snippet)

    # TODO: implement multiple deletions from a single prompt
    rm = subparser.add_parser('rm', help='Remove a snippet')
    rm.add_argument('name', help='Snippet name')
    rm.set_defaults(func=usages.remove_snippet)

    # TODO: implement search logic when "snippet" is passed
    show = subparser.add_parser('show', help='Show all snippets')
    show.add_argument('name', nargs='?', default='', help='Snippet name')
    show.set_defaults(func=usages.show_snippets)

    init = subparser.add_parser('init', help='Initialize Pin configuration file')
    init.set_defaults(func=usages.initialize)

    return parser
