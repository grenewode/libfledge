#!/usr/bin/env python3

import argparse
import json
from typing import Optional

import libfledge
import libfledge.nodes
from libfledge.nodes import Node
from libfledge.interface import to_dict


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


def run_cli(node: Node, pretty: bool = False):
    _show(node.info(), pretty)

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

        reply = node.node_verbs[command_name](
            node, command.get('arguments', {}))
        _show_reply(command_name, reply, pretty)

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
