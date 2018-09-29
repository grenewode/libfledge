from enum import Enum
from types import FunctionType
from typing import Optional

_LIBFLEDGE_FUNC_VERB_TAG = 'libfledge_verb'


class Mode(Enum):
    READ = 'read'
    UPDATE = 'UPDATE'


class Verb:

    def __init__(self, mode: Mode, func: FunctionType, name: Optional[str] = None, desc: Optional[str] = None) -> None:
        self.func = func
        self.mode = mode
        self._name = name
        self._desc = desc

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


def read(*args, **kwargs):
    def decorator(func: FunctionType):
        setattr(func, _LIBFLEDGE_FUNC_VERB_TAG,
                Verb(Mode.READ, func, *args, **kwargs))
        return func

    return decorator


def update(*args, **kwargs):
    def decorator(func: FunctionType):
        setattr(func, _LIBFLEDGE_FUNC_VERB_TAG,
                Verb(Mode.UPDATE, func, *args, **kwargs))
        return func

    return decorator
