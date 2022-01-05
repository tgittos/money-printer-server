from flask import abort
from flask.views import MethodView

from api.lib.constants import API_PREFIX


class BaseApi(MethodView):

    api_base = f"/{API_PREFIX}"

    def __init__(self, url, name):
        self.name = name
        self.url_base = f"{self.api_base}{url}"

    def register_api(self, app, pk='id', pk_type='int', expose_delete=False):
        self.add_url(app, "/", f"get_{self.name}s")
        self.add_url(app, "/", f"create_{self.name}", methods=['POST',])
        self.add_url(app, f"/<{pk_type}:{pk}>", f"get_{self.name}", methods=['GET',])
        self.add_url(app, f"/<{pk_type}:{pk}>", f"update_{self.name}", methods=['PUT',])
        if expose_delete:
            self.add_url(app, f"/<{pk_type}:{pk}>", f"delete_{self.name}" ,methods=['DELETE',])

    def add_url(self, app, url, endpoint=None, view_func=None, methods=['GET',]):
        final_view_func = view_func or self.as_view(self.name)
        final_url = f"{self.url_base}{url}"
        final_endpoint = endpoint or None
        #if self.name not in app.view_functions:
        print(f'registering url: {final_url} under name {final_endpoint} for methods {methods}')
        app.add_url_rule(
            final_url,
            endpoint=final_endpoint,
            view_func=final_view_func,
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
