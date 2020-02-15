from wsgiref import simple_server


def app(environ, start_response):
    response_body = [f'{k}: {v}' for k, v in sorted(environ.items())]
    response_body = '\n'.join(response_body)
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'),]
    start_response(status, response_headers)
    return [response_body.encode('utf8')]


with simple_server.make_server('localhost', 8000, app) as http_server:
    http_server.serve_forever()
