import pytest

from endymion import Endymion
from endymion import exceptions
from endymion.views import View


FILE_DIR = 'css'
FILE_NAME = 'main.css'
FILE_CONTENTS = 'body { background-color: red }'


def create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)

    return asset


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

    with pytest.raises(exceptions.RouteAlreadyExists):
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


def test_cbv_handler_not_implemented(app, client):

    @app.route('/book')
    class BookResource(View):

        def get(self, request):
            return 'response'

    response = client.post('http://testserver/book')

    assert response.status_code == 500
    assert response.text == 'Method not allowed'


def test_alternative_route(app, client):
    RESPONSE_TEXT = 'Alternative way to add a route'

    def index(request):
        return RESPONSE_TEXT

    app.add_route('/alternative', index)

    response = client.get('http://testserver/alternative')
    assert response.text == RESPONSE_TEXT


def test_template(app, client):
    @app.route('/html')
    def html(request):
        return app.template(
            'index.html',
            context={'title': 'Some title', 'name': 'Some name'}
        )

    response = client.get('http://testserver/html')
    assert 'text/html' in response.headers['Content-Type']
    assert 'Some title' in response.text
    assert 'Some name' in response.text


def test_custom_exception_handler(app, client):
    RESPONSE_TEXT = 'AttributeErrorHappend'

    @app.add_exception_handler(AttributeError)
    def on_exception(request, exc):
        return RESPONSE_TEXT

    @app.route('/exception')
    def index(request):
        raise AttributeError()

    response = client.get('http://testserver/exception')

    assert response.text == RESPONSE_TEXT


def test_404_is_returned_for_nonexistent_static_file(client):
    response = client.get('http://testserver/main.css')

    assert response.status_code == 404


def test_assers_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp('static')
    create_static(static_dir)
    app = Endymion(static_dir=str(static_dir))
    client = app.test_session()

    response = client.get(f'http://testserver/{FILE_DIR}/{FILE_NAME}')
    assert response.status_code == 200
    assert response.text == FILE_CONTENTS
