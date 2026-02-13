from argparse import Namespace

from .config import CONFIG_PATH
from .jsonIO import save_config, load_config


def print_snippet(args: Namespace):
    config = load_config(CONFIG_PATH)

    if args.name not in config:
        raise ValueError(f'snippet {args.name} not found')
    else:
        print(config[args.name])


def add_snippet(args: Namespace):
    config = load_config(CONFIG_PATH)

    if args.name in config:
        raise ValueError(f'snippet "{args.name}" already exists')

    config[args.name] = args.cmd
    save_config(CONFIG_PATH, config)


def remove_snippet(args: Namespace):
    config = load_config(CONFIG_PATH)

    if args.name not in config:
        raise ValueError(f'snippet "{args.name}" do not exists')

    config.pop(args.name, None)
    save_config(CONFIG_PATH, config)


def show_snippets(args: Namespace):    
    config = load_config(CONFIG_PATH)

    # TODO: search logic

    print(f"{'SNIPPET':<15} | {'COMMAND'}")
    for name, cmd in config.items():
        print(f"{name:<15} | {cmd}")


# TODO
def initialize():
    pass
