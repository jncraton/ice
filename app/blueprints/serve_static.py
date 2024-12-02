""" Blueprint for serving static HTML, CSS, and JS files """

from flask import Blueprint, request

serve_static = Blueprint("serve_static", __name__, static_folder="../../www")


# Web server routing
@serve_static.route("/")
def serve_root():
    """Return index.html when the page is first loaded"""
    return serve_static.send_static_file("index.html")


@serve_static.route("/<filename>.html")
@serve_static.route("/<filename>.js")
@serve_static.route("/<filename>.css")
def serve_site(filename):
    """Correctly route all elements within the `www` directory"""
    # pylint: disable=unused-argument
    return serve_static.send_static_file(request.path.lstrip("/"))
