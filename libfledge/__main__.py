import nodes
from typing import List, Any


@nodes.node()
class MyNode:

    def __init__(self):
        pass

    @nodes.get()
    def get_10(self):
        return 10


import tornado.ioloop
import tornado.web


def make_app(app_nodes: List[Any]):
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("<h1>Hello From Libfledge</h1>")
            self.write("<ul>")
            for node in app_nodes:
                meta = nodes.get_node_meta(node)
                self.write(
                    "<li><a href={href}>{name}</a></li>".format(href='/' + meta.name, name=meta.name))
            self.write("</ul>")

    def node_handler(node: Any):
        node_meta: nodes.Node = nodes.get_node_meta(node)

        class NodeHandler(tornado.web.RequestHandler):
            def get(self):
                self.write("<h1>Hello From Libfledge @ {}</h1>".format(node_meta.name))
                self.write("<ul>")
                for verb in node_meta.verbs:
                    self.write(
                        "<li><a href={href}>{name}</a></li>".format(href='/' + node_meta.name + "/" + verb.name, name=verb.name))
                self.write("</ul>")

        return (r"/" + node_meta.name, NodeHandler)

    def verb_handler(node: Any, verb: nodes.Verb):
        class VerbHandler(tornado.web.RequestHandler):
            def get(self):
                self.write(str(verb.func(node)))

        return (r"/" + nodes.get_node_meta(node).name + r"/"  +verb.name, VerbHandler)

    routes = [
        (r"/", MainHandler),
    ]

    routes += list(map(node_handler, app_nodes))
    routes += [verb_handler(node, verb) for node in app_nodes for verb in nodes.get_node_meta(node).verbs]

    print(routes)

    return tornado.web.Application(routes)


if __name__ == "__main__":
    node = MyNode()

    app = make_app([node])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
