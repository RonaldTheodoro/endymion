import re

import webob

import utils


class API(object):

    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = webob.Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):

        def wrapper(handler):
            compiled_path = utils.build_route_regexp(path)

            if compiled_path not in self.routes:
                self.routes[compiled_path] = handler
                return handler

        return wrapper

    def handle_request(self, request):
        response = webob.Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            path_params = path.match(request_path)
            if path_params is not None:
                return handler, path_params.groupdict()

    def default_response(self, response):
        response.status_code = 404
        response.text = 'Not found.'
