from typing import List, Mapping, Optional, Union

from libfledge.verbs import _LIBFLEDGE_FUNC_VERB_TAG, Mode, Verb


class VerbGroup:
    def __init__(self,
                 mode: Mode,
                 members: Optional[Mapping[str, Verb]] = None):
        self.mode = mode
        self.members = members if members is not None else {}

    def __iter__(self):
        return iter(self.members)

    def __getattr__(self, name: str) -> Optional[Verb]:
        return self.members[name]

    def __getitem__(self, name: str) -> Optional[Verb]:
        return self.members[name]

    def __setitem__(self, name: str, verb: Verb):
        self.members[name] = verb

    def __contains__(self, item: Union[str, Verb]) -> bool:
        if isinstance(item, Verb):
            return item.name in self
        return item in self.members

    def to_dict(self):
        return {
            'mode': self.mode.value,
            'members':
            {name: member.to_dict()
             for name, member in self.members.items()}
        }


class NodeVerbs:
    def __init__(self,
                 get: Optional[VerbGroup] = None,
                 update: Optional[VerbGroup] = None):
        self.get = get if get is not None else VerbGroup(Mode.GET)
        self.update = update if update is not None else VerbGroup(Mode.UPDATE)

    def add(self, verb: Verb):
        if verb.mode.value == Mode.GET.value:
            self.get[verb.name] = verb
        elif verb.mode.value == Mode.UPDATE.value:
            self.update[verb.name] = verb

    def to_dict(self):
        return {
            Mode.GET.value: self.get.to_dict(),
            Mode.UPDATE.value: self.update.to_dict()
        }


class Node:
    _node_verbs: Optional[NodeVerbs] = None

    def kind_name(self) -> str:
        return type(self).__name__

    def kind_description(self) -> Optional[str]:
        return type(self).__doc__

    @classmethod
    def get_node_verbs(cls) -> NodeVerbs:
        if cls._node_verbs is None:
            cls._node_verbs = NodeVerbs()
            for name in dir(cls):
                attr = getattr(cls, name)
                verb = getattr(attr, _LIBFLEDGE_FUNC_VERB_TAG, None)
                if verb is not None:
                    cls._node_verbs.add(verb)
        return cls._node_verbs
