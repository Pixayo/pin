from argparse import Namespace

from .config import CONFIG_PATH
from .jsonIO import save_config


# TODO: extra argument for "--list", searching snippets by reference

def modify_snippets(config: dict, args: Namespace):
    snippet = args.snippet

    if not snippet:
        raise ValueError('snippet not specified')
    elif snippet in config and args.add:
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


def list_snippets(config: dict):    
    print(f"{'SNIPPET':<15} | {'COMMAND'}")
    for name, command in config.items():
        print(f"{name:<15} | {command}")
