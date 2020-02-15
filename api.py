import re

import webob


class API(object):

    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = webob.Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):

        def wrapper(handler):
            compiled_path = self.build_route_regexp(path)

            if compiled_path not in self.routes:
                self.routes[compiled_path] = handler
                return handler

        return wrapper

    @classmethod
    def build_route_regexp(cls, path):
        named_groups = lambda match: f'(?P<{match.group(1)}>[a-zA-Z0-9_-]+)'

        regex_str = re.sub(r'{([a-zA-Z0-9_-]+)}', named_groups, path)
        return re.compile(f'^{regex_str}$')

    def handle_request(self, request):
        response = webob.Response()

        handler, path_params = self.find_handler(request.path)

        if handler is not None:
            handler(request, response, **path_params.groupdict())
        else:
            self.default_response(response)

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            path_params = path.match(request_path)
            if path_params is not None:
                return handler, path_params

    def default_response(self, response):
        response.status_code = 404
        response.text = 'Not found.'
