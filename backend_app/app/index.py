from web_server.wsgi_handler import (
    WSGIHandler,
    JsonResponse,
    HttpResponseBadRequest,
    g,
)
from playhouse.shortcuts import model_to_dict

from app.models import (
    db,
    Player,
    Club,
    Nationality,
)
from app.utils import TeamBuilder, CanNotBuildException

app = WSGIHandler()


# @app.before_request()
# def open_db_connection(request):
#     g.db = db
#     g.db.connect()


# @app.after_request()
# def close_db_connection(response):
#     g.db.close()
#     return response


def search_players(query, search_string):
    return query.where(
        Player.name.contains(search_string)
        | Nationality.name.contains(search_string)
        | Club.name.contains(search_string)
    ).distinct()


@app.route("/players/")
def get_players(request):
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


@app.route("/best_team/")
def get_best_team(request):
    total = request.query_params.get("total")
    total = int(total)
    try:
        team_arr = TeamBuilder(total=total).get_team()
    except CanNotBuildException as e:
        return HttpResponseBadRequest(request, {"detail": e.message})

    team_ids = [player.get("id") for player in team_arr]
    query = (
        Player.select(Player)
        .where(Player.id.in_(team_ids))
        # .join(Club, on=(Player.club == Club.id))
        # .switch(Player)
        # .join(Nationality, on=(Player.nationality == Nationality.id))
    )
    players = [model_to_dict(item) for item in query]
    res_body = {
        "players": players,
        "total": sum([player.get("value") or 0 for player in players])
    }
    return JsonResponse(request, res_body)
