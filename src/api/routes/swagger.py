import os
from flask import Blueprint, request, redirect, abort, send_from_directory

from api.lib.constants import API_PREFIX

swagger_bp = Blueprint('swagger', __name__)


@swagger_bp.route('/', methods=['GET'])
@swagger_bp.route('/api', methods=['GET'])
@swagger_bp.route('/api/', methods=['GET'])
def redirect_swagger():
    return redirect()


@swagger_bp.route(f"/{API_PREFIX}", methods=['GET'])
@swagger_bp.route(f"/{API_PREFIX}/", methods=['GET'])
@swagger_bp.route(f"/{API_PREFIX}/<path:path>", methods=['GET'])
def serve_swagger(path=None):
    doc_path = os.path.dirname(__file__) + \
        "/../../../docs/swagger/"
    if path is None or path == "":
        return send_from_directory(doc_path, "index.html")
    return send_from_directory(doc_path, path)
