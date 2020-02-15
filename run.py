from wsgiref import simple_server

from app import app


with simple_server.make_server('localhost', 8000, app) as server:
    server.serve_forever()
