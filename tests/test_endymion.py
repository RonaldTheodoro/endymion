import pytest


def test_basic_route_adding(app):
    @app.route('/home')
    def index(request):
        return 'YOLO'

    assert '/home' in app.routes


def test_route_overlap_throws_exception(app):
    @app.route('/home')
    def index(request):
        return 'YOLO'

    assert '/home' in app.routes

    with pytest.raises(AssertionError):
        @app.route('/home')
        def index02(request):
            return 'YOLO'


def test_endymion_test_client_can_send_requests(app, client):
    RESPONSE_TEXT = "I'll be back"

    @app.route('/terminator')
    def terminator(request):
        return RESPONSE_TEXT

    response = client.get('http://testserver/terminator')
    assert response.text == RESPONSE_TEXT


def test_parameterized_route(app, client):
    @app.route('/{name}')
    def say_hello(request, name):
        return f'hey {name}'

    response = client.get('http://testserver/shimira')
    assert response.text == 'hey shimira'
