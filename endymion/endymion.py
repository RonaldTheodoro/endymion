import inspect
import os

import jinja2
import parse
import requests
import webob
import whitenoise
import wsgiadapter


class Endymion(object):

    def __init__(self, templates_dir='templates', static_dir='static'):
        self.routes = {}

        self.templates_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.abspath(templates_dir))
        )

        self.exception_handler = None

        self.whitenose = whitenoise.WhiteNoise(self.wsgi_app, root=static_dir)
    
    def __call__(self, environ, start_response):
        return self.whitenose(environ, start_response)

    def wsgi_app(self, environ, start_response):
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

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = handler()

                response = handler(request, **kwargs)
            else:
                response = self.default_response()
        except Exception as err:
            if self.exception_handler is None:
                raise err
            else:
                response = self.exception_handler(request, err)

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

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler
