import pytest

from endymion.views import View


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


def test_default_404_response(client):
    response = client.get('http://testserver/acme')

    assert response.status_code == 404
    assert response.text == 'Not found.'


def test_cbv_get(app, client):
    RESPONSE_TEXT = 'GET response'

    @app.route('/book')
    class BookResource(View):

        def get(self, request):
            return RESPONSE_TEXT

    response = client.get('http://testserver/book')
    assert response.text == RESPONSE_TEXT


def test_cbv_post(app, client):

    @app.route('/book')
    class BookResource(View):

        def post(self, request):
            book = request.POST['book']
            return f'Book: {book}'

    response = client.post(
        'http://testserver/book',
        data={'book': 'Fluent Python'}
    )
    assert response.text == 'Book: Fluent Python'
