from typing import Mapping, Callable, Any, Type, Optional, Union, List
import inspect
import json

import libfledge
from libfledge import nodes


def to_dict(obj: Any) -> bool:
    if hasattr(obj, 'to_dict') and callable(obj.to_dict):
        return obj.to_dict()
    return obj
