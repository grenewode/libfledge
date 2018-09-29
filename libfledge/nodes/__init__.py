import random
from typing import List, Optional

from verbs import Verb, _LIBFLEDGE_FUNC_VERB_TAG


class Node:
    _node_verbs: Optional[List[Verb]] = None

    def __init__(self):
        self.fledge_id = random.randint(0, 2 ** 64)

    @classmethod
    def kind_name(cls) -> str:
        return cls.__name__

    @classmethod
    def kind_description(cls) -> Optional[str]:
        return cls.__doc__

    def node_verbs(self) -> List[Verb]:
        cls = type(self)

        if cls._node_verbs is not None:
            return cls._node_verbs
        else:
            cls._node_verbs = []
            for name in dir(cls):
                attr = getattr(cls, name)
                verb = getattr(attr, _LIBFLEDGE_FUNC_VERB_TAG, None)
                if verb is not None:
                    cls._node_verbs.append(verb)
            return cls._node_verbs
