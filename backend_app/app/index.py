from web_server.wsgi_handler import (
    WSGIHandler,
    JsonResponse,
    g,
)
from playhouse.shortcuts import model_to_dict

from app.models import (
    db,
    Player,
    Club,
    Nationality,
)

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


def search_players(query, search_string):
    return query.where(
        Player.name.contains(search_string)
        | Nationality.name.contains(search_string)
        | Club.name.contains(search_string)
    ).distinct()


@app.route("/players/")
def get_players(request):
    search_string = request.query_params.get("search")
    query = (
        Player.select(Player, Nationality, Club)
        .join(Club, on=(Player.club == Club.id))
        .switch(Player)
        .join(Nationality, on=(Player.nationality == Nationality.id))
    )

    search_string = request.query_params.get("search")
    if search_string:
        query = search_players(query, search_string)

    res_body = [model_to_dict(item, recurse=True) for item in query]
    return JsonResponse(request, res_body)

    return JsonResponse(request, res_body)
