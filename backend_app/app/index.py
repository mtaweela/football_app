import json
from web_server.wsgi_handler import WSGIServer

app = WSGIServer()


@app.route("/")
def index(env, start_response):
    start_response("200 OK", [("Content-Type", "application/json")])

    response_body = json.dumps({"index": "index"})
    return [bytes(response_body)]


@app.route("/players/")
def get_players(env, start_response):
    start_response("200 OK", [("Content-Type", "application/json")])

    response_body = json.dumps({"players": "players"})
    return [bytes(response_body)]
