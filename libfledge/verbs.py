import json
from enum import Enum
from types import FunctionType
from typing import List, Mapping, Optional, Union, Any, Type
import inspect
from functools import wraps


LIBFLEDGE_VERB_ATTRIBUTE = 'libfledge_verb_attribute'


class Mode(Enum):
    GET = 'get'
    UPDATE = 'update'


class ArgInfo:

    def __init__(self, docs: Optional[str] = None, values: Optional[List[Any]] = None, types=Optional[List[Type]]):
        self.docs = docs
        self.values = values
        self.types = types

    def to_dict(self):
        return {
            "docs": self.docs
        }


class Verb:
    def __init__(self, mode: Mode, func: FunctionType, args: Mapping[str, ArgInfo]):
        self.mode = mode
        self.func = func
        self.args = args

    def __call__(self, instance, kwargs):
        return self.func(instance, **kwargs)

    @property
    def name(self):
        return self.func.__name__

    @property
    def docs(self):
        return (inspect.getdoc(self.func) or '').replace('\n', '\n\t').strip()

    def __str__(self):
        return f'[{self.mode.value}] {self.name}: {self.docs}'

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.docs,
            'mode': self.mode.value,
            'arguments': [arg.to_dict() for arg in self.args]
        }


def get(**kwargs):
    def decorator(func: FunctionType):
        setattr(func, LIBFLEDGE_VERB_ATTRIBUTE, Verb(Mode.GET, func, kwargs))
        return func
    return decorator


def update(**kwargs):
    def decorator(func: FunctionType):
        setattr(func, LIBFLEDGE_VERB_ATTRIBUTE,
                Verb(Mode.UPDATE, func, kwargs))
        return func
    return decorator


class Verbs:

    def __init__(self, node: 'Node', mode: Optional[Mode] = None):
        self.node = node
        self.mode = mode

        self.verbs = {member.name: member for member in filter(lambda member: member is not None, map(lambda i: getattr(
            i[1], LIBFLEDGE_VERB_ATTRIBUTE, None), inspect.getmembers(self.node)))}

    def __iter__(self):
        return iter(self.verbs.values())

    def __getattr__(self, item):
        if item in self.verbs:
            return self.verbs[item]
        raise AttributeError()

    def __getitem__(self, item):
        return self.verbs[item]

    def __contains__(self, item):
        return item in self.verbs

    @property
    def get(self):
        return Verbs(self.node, Mode.GET)

    @property
    def update(self):
        return Verb(self.node, Mode.UPDATE)

    def to_dict(self):
        return {'mode': None if self.mode is None else self.mode.value,
                'verbs': [verb.to_dict() for verb in self]}
