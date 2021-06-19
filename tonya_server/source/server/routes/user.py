from source.server.app import app

@app.route("/")
def index():
    return "Hello World!"