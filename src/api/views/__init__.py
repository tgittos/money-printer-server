import sys
import inspect
import re
import os
import importlib.util
import glob

from .webhooks import webhooks_bp
from .health import health_bp
from .swagger import swagger_bp

def register_api(app):
    """
    Iterates through all available views and registers them with
    the application if they can be registered.
    """
    current_dir = os.path.dirname(__file__)
    for path in glob.glob(current_dir + "/**/*.py", recursive=True):
        basename = os.path.basename(path)

        if basename == "__init__.py" or re.search(r'_test.py$', basename):
            continue
        
        mod_name = basename.split('.')[0]
        spec = importlib.util.spec_from_file_location(mod_name, path)
        mod = importlib.util.module_from_spec(spec)

        #import the module into this package
        spec.loader.exec_module(mod)

        # fetch the actual class from the module
        mod_name_parts = mod_name.split('_')
        cls_name = ''.join(p.title() for p in mod_name_parts) + "Api"
        if cls_name == "BaseApi":
            continue
        if hasattr(mod, cls_name):
            cls = getattr(mod, cls_name)
        else:
            continue

        # create a new instance of this view function
        obj = cls()

        # register with app if valid
        if hasattr(obj, 'register_api'):
            obj.register_api(app)

    
    # Manually register a few lower level APIs we don't expose to the user
    app.register_blueprint(health_bp)
    
    # Manually register the webhook blueprint, since it's not a full Api class
    app.register_blueprint(webhooks_bp)


def register_swagger(app):
    """
    Registers urls for accessing SwaggerUI through the API
    """
    app.register_blueprint(swagger_bp)