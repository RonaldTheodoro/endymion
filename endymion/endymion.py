import inspect
import logging
import os

import jinja2
import parse
import requests
import webob
import whitenoise
import wsgiadapter

from endymion import exceptions


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


class Endymion(object):

    def __init__(self, templates_dir='templates', static_dir='static'):
        self.routes = {}

        self.templates_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.abspath(templates_dir))
        )

        self.exception_handler = {}

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
        if path in self.routes:
            raise exceptions.RouteAlreadyExists()

        logging.info('Adding handler to %s route', path)
        self.routes[path] = handler

    def handle_request(self, request):

        try:
            handler, kwargs = self.find_handler(request.path)
            response = self.execute_handler(request, handler, **kwargs)
        except exceptions.HTTPError as err:
            logging.exception('A HTTP error happend')
            response = webob.Response(body=err.msg, status=err.status_code)
        except exceptions.EndymionBaseException as err:
            logging.exception('An expected error happend')
            response = webob.Response(body=err.msg, status=500)
        except Exception as err:
            logging.exception('An unexpected error happend')
            response = webob.Response(
                body='An internal error happend',
                status=500
            )

        if isinstance(response, str):
            response = webob.Response(body=response)

        return response

    def execute_handler(self, request, handler, **kwargs):
        try:
            if inspect.isclass(handler):
                handler = handler()

            response = handler(request, **kwargs)
        except Exception as err:
            response = self.check_exception_handler(err, request)

        return response

    def check_exception_handler(self, err, request):
        for exc, handler in self.exception_handler.items():
            if isinstance(err, exc):
                logging.warning(
                    'The exception handler %s will be called',
                    handler.__name__
                )
                return handler(request, err)

        logging.warning(
            'Was not found a handler for this exception, it will be reraise'
        )
        raise err

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse.parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        raise exceptions.NotFound()

    def test_session(self, base_url='http://testserver'):
        session = requests.Session()
        session.mount(prefix=base_url, adapter=wsgiadapter.WSGIAdapter(self))
        return session

    def template(self, template_name, context=None):
        if context is None:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exc):

        def wrapper(handler):
            logging.info(
                'Adding %s handler to exception %s',
                handler.__name__,
                repr(exc)
            )
            self.exception_handler[exc] = handler
            return handler

        return wrapper
