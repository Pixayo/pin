import sys
from argparse import Namespace

from .config import CONFIG_PATH
from .jsonIO import save_config, create_config


def print_snippet(args: Namespace, config: dict):

    if args.name not in config:
        raise KeyError(f'snippet "{args.name}" not found')
    else:
        print(config[args.name])


def add_snippet(args: Namespace, config: dict):

    if args.name in config:
        raise ValueError(f'snippet "{args.name}" already exists')

    config[args.name] = args.cmd
    save_config(CONFIG_PATH, config)


def remove_snippet(args: Namespace, config: dict):

    if args.name not in config:
        raise ValueError(f'snippet "{args.name}" do not exists')

    config.pop(args.name, None)
    save_config(CONFIG_PATH, config)


# TODO: search logic
def show_snippets(args: Namespace, config: dict):    
    
    header = f"{'SNIPPET':<15} | {'COMMAND'}"
    
    rows = [f"{name:<15} | {cmd}" for name, cmd in config.items()]
    
    result = "\n".join([header] + rows)

    print(result, file=sys.stderr)


# TODO: need more testing
def initialize():
    create_config(CONFIG_PATH)
