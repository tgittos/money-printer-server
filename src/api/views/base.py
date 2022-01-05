from flask import abort
from flask.views import MethodView

from api.lib.constants import API_PREFIX


class BaseApi(MethodView):

    api_base = f"/{API_PREFIX}"

    def __init__(self, url, name):
        self.name = name
        self.url_base = f"{self.api_base}{url}"

    def register_api(self, app, pk='id', pk_type='int', expose_delete=False):
        bulk_methods = ['GET', 'PUT']
        if expose_delete:
            bulk_methods.append('DELETE')
        self.add_url(app, "/")
        self.add_url(app, "/", methods=['POST',])
        self.add_url(app, f'/<{pk_type}:{pk}>', methods=bulk_methods)

    def add_url(self, app, url, view_func=None, methods=['GET',]):
        final_url = f"{self.url_base}{url}"
        if self.name not in app.view_functions:
            app.add_url_rule(
                final_url,
                view_func=view_func or self.as_view(self.name),
                methods=methods
            )

    def get(self, id):
        abort(404)

    def post(self):
        abort(404)

    def delete(self, id):
        abort(404)

    def put(self, id):
        abort(404)
