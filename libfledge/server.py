import flask
import flask.json

from nodes import Node


def create_server(name: str, *args: Node) -> flask.Flask:
    app = flask.Flask(name)

    nodes = {node.fledge_id: node for node in args}
    print(nodes)

    @app.route('/', methods=['GET'])
    def index():
        return flask.jsonify([str(node.fledge_id) for node in args])

    @app.route('/<node_id>', methods=['GET'])
    def get_node(node_id: str):
        node = nodes[int(node_id)]

        response = {'id': node.fledge_id,
                    'kind': node.kind_name()}
        description = node.kind_description()
        if description is not None:
            response['description'] = description

        return flask.jsonify(response)

    return app
