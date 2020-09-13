import json


class Router(object):
    def __init__(self):
        self.routes = {}

    def assign(self, path, function):
        self.routes[path] = function

    def get_controller(self, path):
        controller = self.routes.get(path)
        if not controller:
            raise Http404()
        return controller


class WSGIServer(object):
    def __init__(self):
        self.router = Router()

    def __call__(self, env, start_response):
        return self._handle_request(env, start_response)

    def _handle_request(self, env, start_response):
        path_info = env.get("PATH_INFO")
        try:
            controller = self.router.get_controller(path_info)
        except Http404 as e:
            start_response("500", [("Content-Type", "application/json")])
            response_body = json.dumps({"error": e.message})
            return [bytes(response_body)]
        return controller(env, start_response)

    def route(self, path=None):
        if not path:
            raise Exception("path is reuquired.")

        def wrapper(function):
            self.router.assign(path, function)

        return wrapper

    def before_request(self, *args, **kwargs):
        def wrapper(function):
            pass

        return wrapper

    def after_request(self, *args, **kwargs):
        def wrapper(function):
            pass

        return wrapper


# ----- Response


class HttpResponseBase:
    pass


class HttpResponse(HttpResponseBase):
    status_code = 200
    content_type = "text/html"
    content = ""


class JsonResponse(HttpResponseBase):
    status_code = 200
    content_type = "application/json"
    content = {}


class HttpResponseBadRequest(JsonResponse):
    status_code = 400


class HttpResponseNotFound(JsonResponse):
    status_code = 404


class HttpResponseServerError(JsonResponse):
    status_code = 500


# ----- Exciptoins


class Http404(Exception):
    message = "not found"
