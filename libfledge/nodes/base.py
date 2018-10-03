from typing import List, Mapping, Optional

from libfledge.verbs import _LIBFLEDGE_FUNC_VERB_TAG, Mode, Verb


class Node:
    def kind_name(self) -> str:
        return type(self).__name__

    def kind_description(self) -> Optional[str]:
        return type(self).__doc__

    # def _do_node_verb(self, mode: Mode, name: str, args: Mapping[str, str]):
    #     getter = getattr(type(self), name, None)
    #     if getter is not None:
    #         verb = getattr(getter, _LIBFLEDGE_FUNC_VERB_TAG, None)
    #         if verb is not None and verb.mode.value == mode.value:
    #             return verb.func(self, **args)
    #
    # def do_node_getter(self, name: str, args: Mapping[str, str]):
    #     return self._do_node_verb(Mode.READ, name, args)
    #
    # def do_node_updater(self, name: str, args: Mapping[str, str]):
    #     return self._do_node_verb(Mode.UPDATE, name, args)
    

    @classmethod
    def get_node_verbs(cls) -> Mapping[str, Mapping[str, Verb]]:
        node_verbs: Mapping[str, Mapping[str, Verb]] = {}
        for name in dir(cls):
            attr = getattr(cls, name)
            verb = getattr(attr, _LIBFLEDGE_FUNC_VERB_TAG, None)
            if verb is not None:
                node_verbs.setdefault(verb.mode.value)[verb.mode.value] = verb
        return node_verbs
