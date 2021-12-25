import os
from flask import Blueprint, request, Response, abort, send_from_directory

swagger_bp = Blueprint('swagger', __name__)


@swagger_bp.route('/v1/api', methods=['GET'])
@swagger_bp.route('/v1/api/', methods=['GET'])
@swagger_bp.route('/v1/api/<path:path>', methods=['GET'])
def serve_swagger(path=None):
    doc_path = os.path.dirname(__file__) + \
        "/../../../docs/swagger/"
    if path is None or path == "":
        return send_from_directory(doc_path, "index.html")
    return send_from_directory(doc_path, path)
