from typing import List, Optional, Mapping

from libfledge.verbs import Verb, _LIBFLEDGE_FUNC_VERB_TAG, Mode


class Node:
    def kind_name(self) -> str:
        return type(self).__name__

    def kind_description(self) -> Optional[str]:
        return type(self).__doc__

    def node_getters(self) -> List[Verb]:
        return self._node_verbs(Mode.READ)

    def _do_node_verb(self, mode: Mode, name: str, args: Mapping[str, str]):
        getter = getattr(type(self), name, None)
        if getter is not None:
            verb = getattr(getter, _LIBFLEDGE_FUNC_VERB_TAG, None)
            if verb is not None and verb.mode.value == mode.value:
                return verb.func(self, **args)

    def do_node_getter(self, name: str, args: Mapping[str, str]):
        return self._do_node_verb(Mode.READ, name, args)

    def do_node_updater(self, name: str, args: Mapping[str, str]):
        return self._do_node_verb(Mode.UPDATE, name, args)

    def node_updaters(self) -> List[Verb]:
        return self._node_verbs(Mode.UPDATE)

    def _node_verbs(self, mode: Mode) -> List[Verb]:
        cls = type(self)
        node_verbs = []
        for name in dir(cls):
            attr = getattr(cls, name)
            verb = getattr(attr, _LIBFLEDGE_FUNC_VERB_TAG, None)
            if verb is not None and verb.mode.value == mode.value:
                node_verbs.append(verb)
        return node_verbs
