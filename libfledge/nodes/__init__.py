from typing import Mapping

from libfledge.nodes.base import Node
from libfledge.nodes.weather import *


def kind_name(node: Node):
    return node.kind_name()


def kind_description(node: Node):
    return node.kind_description()


def node_getters(node: Node):
    return node.node_getters()


def node_updaters(node: Node):
    return node.node_updaters()


def do_node_getter(node: Node, name: str, args: Mapping[str, str]):
    return node.do_node_getter(name, args)


def do_node_updater(node: Node, name: str, args: Mapping[str, str]):
    return node.do_node_updater(name, args)
