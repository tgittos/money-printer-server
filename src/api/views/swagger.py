import os
from flask import Blueprint, request, redirect, abort, send_from_directory

from constants import API_PREFIX

swagger_bp = Blueprint('swagger', __name__)


@swagger_bp.route('/', methods=['GET'])
@swagger_bp.route('/api', methods=['GET'])
@swagger_bp.route('/api/', methods=['GET'])
def redirect_swagger():
    if 'MP_ENVIRONMENT' in os.environ and \
        os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
        return redirect(f"/{API_PREFIX}/")
    return '', 404


@swagger_bp.route(f"/{API_PREFIX}", methods=['GET'])
@swagger_bp.route(f"/{API_PREFIX}/", methods=['GET'])
@swagger_bp.route(f"/{API_PREFIX}/<path:path>", methods=['GET'])
def serve_swagger(path=None):
    if 'MP_ENVIRONMENT' in os.environ and \
        os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
        doc_path = os.path.dirname(__file__) + \
            "/../../../docs/swagger/"
        if path is None or path == "":
            return send_from_directory(doc_path, "index.html")
        return send_from_directory(doc_path, path)
    return '', 404