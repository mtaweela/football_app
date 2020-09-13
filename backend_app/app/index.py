from web_server.wsgi_handler import WSGIHandler, JsonResponse, g

from app.models import db, Player

app = WSGIHandler()


@app.before_request()
def open_db_connection(request):
    g.db = db
    g.db.connect()


@app.after_request()
def close_db_connection(response):
    g.db.close()
    return response


@app.route("/")
def index(request):
    return JsonResponse(request, {"index": "index"})


@app.route("/players/")
def get_players(request):
    return JsonResponse(request, {"players": "players"})
