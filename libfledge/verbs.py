from enum import Enum
from types import FunctionType
from typing import List, Mapping, Optional, Union

_LIBFLEDGE_FUNC_VERB_TAG = 'libfledge_verb'


class Mode(Enum):
    GET = 'get'
    UPDATE = 'UPDATE'


class Verb:

    def __init__(self, mode: Mode, func: FunctionType, name: Optional[str], desc: Optional[str], arguments: Mapping[str, type]) -> None:
        self.func = func
        self.mode = mode
        self._name = name
        self._desc = desc

    def __call__(self, **kwargs: object):
        # do typechecking
        for (name, ty) in self.arguments:
            if name not in kwargs:
                raise ValueError(
                    f'{self.name} expects an argument named {name}')
            elif not isinstance(kwargs[name], ty):
                raise TypeError(
                    f'{self.name} expects an argument named {name}')
        return self.func(**kwargs)

    @property
    def name(self):
        return self.func.__name__ if self._name is None else self._name

    @property
    def arguments(self):
        return self.func.__annotations__

    @property
    def description(self):
        return self._desc

    def __str__(self):
        return '[{mode}] {name}(...)'.format(mode=self.mode, name=self.name)

    def __repr__(self):
        return '{}({mode}, {func}, name={name}, desc={desc})'.format(type(self).__name__,
                                                                     mode=self.mode, func=self.func, name=self._name,
                                                                     desc=self._desc)


def get(name: Optional[str] = None, description: Optional[str] = None, **arguments: type):
    def decorator(func: FunctionType):
        setattr(func, _LIBFLEDGE_FUNC_VERB_TAG,
                Verb(Mode.GET, func, name, description, arguments))
        return func

    return decorator


def update(name: Optional[str] = None, description: Optional[str] = None, **arguments: type):
    def decorator(func: FunctionType):
        setattr(func, _LIBFLEDGE_FUNC_VERB_TAG,
                Verb(Mode.UPDATE, func, name, description, arguments))
        return func

    return decorator
