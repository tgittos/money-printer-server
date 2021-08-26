from os import path
from flask import send_from_directory

# static client site routes
root_dir = path.abspath(path.join(path.dirname(__file__), '../client'))
@app.route('/v1/')
@app.route('/v1/index')
def serve_client():
    return send_from_directory(root_dir, 'index.html')

