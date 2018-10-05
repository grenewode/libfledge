#!/usr/bin/env python3

import argparse
import json
from typing import Optional

import libfledge
import libfledge.nodes
from libfledge.nodes import Node, get_node_verbs, kind_description, kind_name
from libfledge.verbs import Mode


def _cli_startup_info(node: Node):
    return {
        'libfledge': {
            'version': libfledge.__version__,
            'paths': libfledge.__path__
        },
    }


def _node_info(node: Node):
    return {
        'kind_name': kind_name(node),
        'kind_description': kind_description(node),
        'verbs': get_node_verbs(node).to_dict()
    }


def to_dict(obj: object) -> bool:
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        return obj.to_dict()
    return obj


def _show(msg: dict, pretty: bool):
    print(json.dumps(msg, indent=4 if pretty else None))


def _show_error(error: Exception, pretty: bool):
    _show({
        'status': 'error',
        'error_name': type(error).__name__,
        'message': str(error)
    }, pretty)


def _show_reply(command: str, msg: object, pretty: bool):
    _show({
        'status': 'ok',
        'command': command,
        'message': to_dict(msg)
    }, pretty)


class Command:
    def __init__(self, args, func):
        self.args = args
        self.func = func

    def __call__(self, node: Node, command: dict):
        return self.func(node, **command)


_COMMANDS = {}


def command(**kwargs):
    def decorator(func):
        global _COMMANDS

        _COMMANDS[func.__name__.strip('_\t ')] = Command(kwargs, func)

        return func

    return decorator


@command(
    mode="optional." +
    "Specifies the which type of verb to list.Valid values are get and update")
def _list_verbs(node: Node, mode: Optional[str] = None):
    """
    Get the list of verbs available on this node.

    Accepts the optional "mode" argument,
    which may have the value 'get' or 'update',
    and is used to filter for a particular type of verb.
    """
    verbs = node.get_node_verbs()
    if mode is not None:
        return verbs[mode]
    else:
        return verbs


@command(
    mode="the mode this verb belongs to",
    verb="the name of the verb to fire",
    arguments="the arguments to the verb")
def _do(node: Node, mode: str, verb: str, arguments: dict):
    verbs = get_node_verbs(node)
    return verbs[mode][verb](node, **arguments)


@command()
def _help(node: Node):
    """
    Shows the help message
    """
    global _COMMANDS

    return {name: func.__doc__ for name, func in _COMMANDS.items()}


def run_cli(node: Optional[Node], pretty: bool = False):
    _show(_cli_startup_info(node), pretty)
    if node is not None:
        _show(_node_info(node), pretty)

    input_buffer = ''
    while True:
        current_line = input()

        # We want to read until we see an empty line
        if current_line:
            input_buffer += current_line
            continue

        # Ok, so the last line was empty, we might have a new command
        # If the input buffer isn't empty, then we have a command to execute
        if not input_buffer:
            continue

        try:
            command = json.loads(input_buffer)
            command_name = command['command']
        except json.decoder.JSONDecodeError as err:
            _show_error(err, pretty)

        try:
            msg = _COMMANDS[command_name](node, command.get('arguments', {}))
            _show_reply(command_name, msg, pretty)
        except Exception as err:
            _show_error(err, pretty)

        # Reset the input buffer so that we can wait for the next command
        input_buffer = ''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--pretty',
        action='store_true',
        default=False,
        help='if the output of commands should be pretty printed')
    parser.add_argument('node', nargs='?', help='the node the load')

    args = parser.parse_args()
    node = None
    if args.node is not None:
        if args.node not in libfledge.nodes.__dict__:
            print(f'unknown node name: {args.node}')
            return

        node_cls = libfledge.nodes.__dict__[args.node]
        if issubclass(node_cls, type(Node)):
            print(f'not a node class: {args.node}')
            return

        # Create the node from it's class.
        # TODO: this should really take some arguments from a config file or something
        node = node_cls()

    run_cli(node, args.pretty)
