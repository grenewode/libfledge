import libfledge
import json
import string
import argparse
from libfledge.nodes import Node
from libfledge.verbs import Mode


def _cli_startup_info(node: Node):
    return {
        'libfledge_version': libfledge.__version__,
        'node': {
            'kind': node.kind_name(),
            'description': node.kind_description()
        }
    }


def to_dict(obj: object) -> bool:
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        return obj.to_dict()
    return obj


def _show(msg: dict, pretty: bool):
    print(json.dumps(msg, ident=4 if pretty else None))


def _show_error(error: Exception, pretty: bool):
    _show({
        'status': 'error',
        'name': type(error).__name__,
        'message': str(error)
    }, pretty)


def _show_reply(command: str, msg: object, pretty: bool):
    _show({'status': 'ok', 'name': command, 'message': to_dict(msg)}, pretty)


_COMMANDS = {}


def command(func):
    global _COMMANDS

    _COMMANDS[string.strip(func.__name__, chars='_\t ')] = func

    return func


@command
def _list_verbs(command: dict, node: Node):
    """
    Get the list of verbs available on this node.

    Accepts the optional "mode" argument,
    which may have the value 'get' or 'update',
    and is used to filter for a particular type of verb.
    """
    verbs = node.get_node_verbs()
    if 'mode' in command or command['mode'] is not None:
        mode = command['mode']
        if mode == Mode.GET.value:
            return verbs.get
        elif mode == Mode.UPDATE.value:
            return verbs.update
    return verbs


def run_cli(node: Node, pretty: bool = False):
    _show_reply(_cli_startup_info(node), pretty)

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

            command_name = command['command_name']
            msg = _COMMANDS[command_name](command, node)
            _show_reply(command_name, msg, pretty)
        except Exception as err:
            _show_error(err, pretty)

        # Reset the input buffer so that we can wait for the next command
        input_buffer = ''


def main():
    parser = argparse.ArgumentParser('launcher for libfledge')
    parser.add_argument(
        'node', metavar='NODE', type=str, help='the node the load')
    parser.add_argument(
        '--pretty', help='if the output of commands should be pretty printed')
    args = parser.parse_args()
    print(args)
