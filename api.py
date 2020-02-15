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
            self.routes[path] = handler
            return handler

        return wrapper

    def handle_request(self, request):
        response = webob.Response()

        handler = self.find_handler(request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler

    def default_response(self, response):
        response.status_code = 404
        response.text = 'Not found.'
