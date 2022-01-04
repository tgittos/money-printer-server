from flask.views import MethodView

from api.lib.constants import API_PREFIX


class BaseApi(MethodView):

    api_base = f"/{API_PREFIX}"

    def __init__(self, url):
        self.view_func = self.as_view(__name__)
        self.url_base = f"{self.api_base}/{url}"

    def register_api(self, app, pk='id', pk_type='int', expose_delete=False):
        bulk_methods = ['GET', 'PUT']
        if expose_delete:
            bulk_methods.append('DELETE')
        self.add_url(app, "/")
        self.add_url(app, "/", methods=['POST',])
        self.add_url(app, f'/<{pk_type}:{pk}>', view_func=self.view_func,
                        methods=bulk_methods)

    def add_url(self, app, url, view_func=None, methods=['GET',]):
        app.add_url_rule(
            f"{self.url_base}/{url}",
            view_func=view_func or self.view_func,
            methods=methods
        )

    def get(self, id):
        if id is None:
            # return a list of users
            pass
        else:
            # expose a single user
            pass

    def post(self):
        # create a new user
        pass

    def delete(self, id):
        # delete a single user
        pass

    def put(self, id):
        # update a single user
        pass
