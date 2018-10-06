import json
from typing import Mapping, Union, Type, Optional
import inspect

import libfledge
from libfledge import verbs


class Node:

    def __init__(self):
        self.node_verbs = verbs.Verbs(self)

    @classmethod
    def cls_info(cls):
        return {'kind_name': cls.cls_kind_name(),
                'kind_description': cls.cls_kind_description()}

    @classmethod
    def cls_kind_name(cls):
        """The kind of node this is"""
        return cls.__name__

    @classmethod
    def cls_kind_description(cls):
        """The description of this node"""
        return inspect.getdoc(cls)

    @verbs.get()
    def info(self):
        """Provides information about this node"""
        return type(self).cls_info()

    @verbs.get()
    def kind_name(self):
        """The kind of node this is"""
        return type(self).cls_kind_name()

    @verbs.get()
    def kind_description(self):
        """The description of this node"""
        return type(self).cls_kind_description()

    @verbs.get()
    def help(self):
        """Shows the help message"""
        return {verb.name: verb.to_dict() for verb in self.node_verbs}


from libfledge.nodes.weather import Weather, NOAA, WeatherCom
