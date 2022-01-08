from flask import abort
from flask.views import MethodView

from constants import API_PREFIX


class BaseApi(MethodView):

    api_base = f"/{API_PREFIX}"

    def __init__(self, url, name):
        self.name = name
        self.url_base = f"{self.api_base}{url}"

    def register_api(self, app, pk='id', pk_type='int', expose_delete=False):
        self.add_url(app, "/", endpoint=f"get_{self.name}s")
        self.add_url(app, "/", endpoint=f"create_{self.name}", methods=['POST',])
        self.add_url(app, f"/<{pk_type}:{pk}>", endpoint=f"get_{self.name}", methods=['GET',])
        self.add_url(app, f"/<{pk_type}:{pk}>", endpoint=f"update_{self.name}", methods=['PUT',])
        if expose_delete:
            self.add_url(app, f"/<{pk_type}:{pk}>", endpoint=f"delete_{self.name}" ,methods=['DELETE',])

    def add_url(self, app, url, view_func=None, endpoint=None, methods=['GET',]):

        final_view_func = view_func or self.as_view(self.name)
        final_endpoint = endpoint or final_view_func.__name__
        final_url = f"{self.url_base}{url}"
        urls = [(final_endpoint, final_url)]
        if final_url.endswith('/'):
            urls.append((final_endpoint + "_alt", final_url[0:-1]))
        else:
            urls.append((final_endpoint + "_alt", final_url + "/"))

        #if self.name not in app.view_functions:
        for url_tuple in urls:
            endpoint, url = url_tuple
            print(f'registering url: {url} for methods {methods} under name {endpoint}')
            app.add_url_rule(
                url,
                endpoint=endpoint,
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
