from web_server.wsgi_handler import WSGIHandler, JsonResponse

app = WSGIHandler()


@app.route("/")
def index(request):
    return JsonResponse(request, {"index": "index"})


@app.route("/players/")
def get_players(request):
    return JsonResponse(request, {"players": "players"})
