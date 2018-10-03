import json
from typing import Mapping, Union

from libfledge.nodes.base import Node
from libfledge.nodes.weather import *
from libfledge.verbs import Verb


def kind_name(node: Node):
    return node.kind_name()


def kind_description(node: Node):
    return node.kind_description()


def get_node_verbs(node: Union[Type[Node], Node]):
    if isinstance(node, Node):
        return get_node_verbs(type(node))
    return node.get_node_verbs()


# def get_node_getters(node: Node) -> Mapping[str, Verb]:
#     return {verb.name: verb for verb in node.node_getters()}
#
#
# def get_node_updaters(node: Node):
#     return {verb.name: verb for verb in node.node_updaters()}
#
#
# def do_node_getter(node: Node, name: str, args: Mapping[str, str]):
#     return json.dumps(node.do_node_getter(name, args))
#
#
# def do_node_updater(node: Node, name: str, args: Mapping[str, str]):
#     return json.dumps(node.do_node_updater(name, args))
