from wsgiref import simple_server


class Reverseware(object):

    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response, *args, **kwargs):
        wrapped_app_response = self.wrapped_app(environ, start_response)
        return [data[::-1] for data in wrapped_app_response]


def app(environ, start_response):
    response_body = [f'{k}: {v}' for k, v in sorted(environ.items())]
    response_body = '\n'.join(response_body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ]
    start_response(status, response_headers)
    return [response_body.encode('utf8')]


with simple_server.make_server('localhost', 8000, Reverseware(app)) as server:
    server.serve_forever()
