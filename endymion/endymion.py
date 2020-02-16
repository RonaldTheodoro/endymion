import inspect

import parse
import requests
import webob
import wsgiadapter


class Endymion(object):

    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = webob.Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):

        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper
    
    def add_route(self, path, handler):
        assert path not in self.routes, 'Such route already exists'

        self.routes[path] = handler

    def handle_request(self, request):
        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = handler()

            response = handler(request, **kwargs)
        else:
            response = self.default_response()

        if isinstance(response, str):
            response = webob.Response(body=response)

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse.parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        else:
            return None, None

    def default_response(self):
        response = webob.Response()
        response.status_code = 404
        response.text = 'Not found.'
        return response

    def test_session(self, base_url='http://testserver'):
        session = requests.Session()
        session.mount(prefix=base_url, adapter=wsgiadapter.WSGIAdapter(self))
        return session
