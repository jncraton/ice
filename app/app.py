from flask import Flask, send_from_directory, request

app = Flask(__name__, static_folder="../www")


@app.route("/")
def serve_root():
    return app.send_static_file("index.html")


@app.route("/<filename>.html")
@app.route("/<filename>.js")
@app.route("/<filename>.css")
def serve_site(filename):
    return app.send_static_file(request.path.lstrip("/"))
