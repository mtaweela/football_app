import json
import logging
import logging.config
import yaml
import os
import importlib
from urllib.parse import parse_qs
from web_server.data_structures import Singleton


# ----- AppGlabals


class AppGlabals(Singleton):
    pass


g = AppGlabals()


# ----- WSGIHandler


class WSGIHandler(object):
    def __init__(self):
        self.router = Router()
        self.middleware_handler = MiddlewareHandler()

    def __call__(self, env, start_response):
        return self._handle_request(env, start_response)

    def _handle_request(self, env, start_response):
        try:
            request = Request(env, start_response)

            controller = self.router.get_controller(request)

            # run pre middlewares before and after request
            self.middleware_handler.run_pre_request(request)
            response = controller(request).write()
            response = self.middleware_handler.run_post_request(response)

            return response
        except Exception as e:
            return ExciptoinsHandler().handle(request, e)

    def route(self, path=None):
        if not path:
            raise Exception("path is reuquired.")

        def wrapper(function):
            self.router.assign(path, function)

        return wrapper

    def before_request(self):
        def wrapper(function):
            self.middleware_handler.assign_pre(function)

        return wrapper

    def after_request(self):
        def wrapper(function):
            self.middleware_handler.assign_post(function)

        return wrapper


# ----- Router


class Router(object):
    def __init__(self):
        self.routes = {}

    def assign(self, path, function):
        self.routes[path] = function

    def get_controller(self, request):
        path = request.env.get("PATH_INFO")
        controller = self.routes.get(path)
        if not controller:
            raise Http404()
        return controller


# ----- MiddlewareHandler


class MiddlewareHandler(object):
    def __init__(self):
        self.pre_request_middlewares = []
        self.post_request_middlewares = []

    def assign_pre(self, function):
        self.pre_request_middlewares.append(function)

    def assign_post(self, function):
        self.post_request_middlewares.append(function)

    def run_pre_request(self, request):
        for middleware in self.pre_request_middlewares:
            middleware(request)

    def run_post_request(self, response):
        for middleware in self.post_request_middlewares:
            response = middleware(response)
        return response


# ----- Request


class Request(object):
    query_params = {}

    def __init__(self, env, start_response):
        self.env = env
        self.start_response = start_response
        self.query_params = self.get_query_params_from_url()

    def get_query_params_from_url(self):
        query = self.env["QUERY_STRING"]
        params = parse_qs(query)
        query_params = {k: v[0] for k, v in params.items()}
        return query_params


# ----- Response


class HttpResponseBase(object):
    status_code = 200
    content_type = "text/html"
    _content = ""

    def __init__(self, request, content="", status=None):
        self.request = request
        self._content = content
        if status:
            self.status_code = status

    def write(self):
        self.request.start_response(
            str(self.status_code), [("Content-Type", self.content_type)]
        )
        return [bytes(self._content, "utf-8")]


class HttpResponse(HttpResponseBase):
    pass


class JsonResponse(HttpResponseBase):
    content_type = "application/json"

    def __init__(self, request, dict_content={}, status=None):
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


# ----- Logger


class Logger(object):
    def __init__(self):
        settings = importlib.import_module(os.environ.get("SETTINGS_MODULE"))
        config_file = settings.LOGGER_CONFIG_FILE

        with open(config_file, "r") as f:
            log_cfg = yaml.safe_load(f.read())

        logging.config.dictConfig(log_cfg)

        self.logger = logging.getLogger("dev")

    def error(self, msg):
        self.logger.setLevel(logging.ERROR)
        self.logger.error(msg)

    def info(self, msg):
        self.logger.setLevel(logging.INFO)
        self.logger.info(msg)


# ----- Exciptoins


class Http404(Exception):
    message = "not found"

    def __str__(self):
        return "http not found"


# ----- Exciptoins Handler


class ExciptoinsHandler(object):
    def handle(self, request, exception):
        if type(exception) == Http404:
            return HttpResponseNotFound(request, {"error": exception.message}).write()
        else:
            Logger().error(exception)
            return HttpResponseServerError(request).write()
