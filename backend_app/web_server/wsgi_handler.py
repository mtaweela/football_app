import json


class WSGIHandler(object):
    def __init__(self):
        self.router = Router()

    def __call__(self, env, start_response):
        return self._handle_request(env, start_response)

    def _handle_request(self, env, start_response):
        request = Request(env, start_response)
        path_info = env.get("PATH_INFO")
        try:
            controller = self.router.get_controller(path_info)
        except Http404 as e:
            return HttpResponseNotFound(request, {"error": e.message}).write()
        return controller(request).write()

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


class MiddlewareHandler(object):
    def __init__(self):
        self.pre_request_middlewares = []
        self.post_request_middlewares = []

    def assign_pre(self, path, function):
        self.pre_request_middlewares.append(function)

    def assign_post(self, path, function):
        self.post_request_middlewares.append(function)

    def run_pre_request(self, env, start_response):
        for middleware in self.pre_request_middlewares:
            middleware(env, start_response)

    def run_post_request(self, env, start_response):
        for middleware in self.post_request_middlewares:
            middleware(env, start_response)


# ----- Request


class Request(object):
    def __init__(self, env, start_response):
        self.env = env
        self.start_response = start_response


# ----- Response


class HttpResponseBase(object):
    status_code = 200
    content_type = "text/html"
    _content = ""

    def __init__(self, request, content, status=None):
        self.request = request
        self._content = content
        if status:
            self.status_code = status

    def write(self):
        self.request.start_response(
            str(self.status_code), [("Content-Type", self.content_type)]
        )
        return [bytes(self._content)]


class HttpResponse(HttpResponseBase):
    pass


class JsonResponse(HttpResponseBase):
    content_type = "application/json"

    def __init__(self, request, dict_content, status=None):
        content = json.dumps(dict_content)
        super(JsonResponse, self).__init__(request, content, status)


class HttpResponseBadRequest(JsonResponse):
    status_code = 400
    content_type = "application/json"
    _content = {"detail": "bad request"}


class HttpResponseNotFound(JsonResponse):
    status_code = 404
    content_type = "application/json"
    _content = {"detail": "not found"}


class HttpResponseServerError(JsonResponse):
    status_code = 500


# ----- Exciptoins


class Http404(Exception):
    message = "not found"
