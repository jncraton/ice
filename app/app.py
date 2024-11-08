"""
    Flask server for running the API for the database and web server for the application. 

    Currently provides routes to all static files in the `www` directory
"""

from flask import Flask, request

app = Flask(__name__, static_folder="../www")


@app.route("/")
def serve_root():
    """Return index.html when the page is first loaded"""
    return app.send_static_file("index.html")


@app.route("/<filename>.html")
@app.route("/<filename>.js")
@app.route("/<filename>.css")
def serve_site():
    """Correctly route all elements within the `www` directory"""
    return app.send_static_file(request.path.lstrip("/"))
