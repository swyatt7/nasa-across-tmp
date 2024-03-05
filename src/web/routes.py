from .app import web_app

@web_app.route("/hello", methods=["GET"])
def web_hello():
    return "WSGI Flask APP says hello"