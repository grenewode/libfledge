from typing import Optional, Any, List
from enum import Enum

LIB_FLEDGE_FUNC_VERB_TAG = 'libfledge_verb'
LIB_FLEDGE_CLASS_NODE_TAG = 'libfledge_node'


class Mode(Enum):
    GET = 'get'
    ACTION = 'action'


class Verb:

    def __init__(self, mode: Mode, func, name: Optional[str] = None, desc: Optional[str] = None):
        self.func = func
        self.mode = mode
        self._name = name
        self._desc = desc

    @property
    def name(self):
        return self.func.__name__ if self._name is None else self._name

    @property
    def description(self):
        return self._desc

    def __str__(self):
        return '[{mode}] {name}(...)'.format(mode=self.mode, name=self.name)

    def __repr__(self):
        return '{}({mode}, {func}, name={name}, desc={desc})'.format(type(self).__name__,
                                                                     mode=self.mode, func=self.func, name=self._name, desc=self._desc)


class Node:
    def __init__(self, clazz, name: Optional[str] = None, desc: Optional[str] = None):
        self.clazz = clazz
        self._name = name
        self._desc = desc
        self.verbs = []

    @property
    def name(self):
        return self.clazz.__name__ if self._name is None else self._name

    @property
    def description(self):
        return self._desc

    def __str__(self):
        return self.name


def get(*args, **kwargs):
    def decorator(func):
        setattr(func, LIB_FLEDGE_FUNC_VERB_TAG,
                Verb(Mode.GET, func, *args, **kwargs))
        return func
    return decorator


def action(*args, **kwargs):
    def decorator(func):
        setattr(func, LIB_FLEDGE_FUNC_VERB_TAG,
                Verb(Mode.ACTION, func, *args, **kwargs))
        return func
    return decorator


def node(*args, **kwargs):

    def decorator(clazz):
        node = Node(clazz)
        for name in dir(clazz):
            attr = getattr(clazz, name)
            verb = getattr(attr, LIB_FLEDGE_FUNC_VERB_TAG, None)
            if verb is not None:
                node.verbs.append(verb)
        setattr(clazz, LIB_FLEDGE_CLASS_NODE_TAG, node)
        return clazz

    return decorator


class ExpectedNodeError(Exception):
    pass


def get_node_meta(node: Any) -> Node:
    if hasattr(node, LIB_FLEDGE_CLASS_NODE_TAG):
        return getattr(node, LIB_FLEDGE_CLASS_NODE_TAG)
    ty = type(node)
    if hasattr(ty, LIB_FLEDGE_CLASS_NODE_TAG):
        return getattr(ty, LIB_FLEDGE_CLASS_NODE_TAG)
    raise ExpectedNodeError()
