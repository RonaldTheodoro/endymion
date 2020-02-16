from endymion import Endymion
from endymion.views import View


app = Endymion()


@app.route('/')
def index(request):
    return 'Hello from index page'


@app.route('/about')
def about(request):
    return 'Hello from about page'


@app.route('/hello/{name}')
def say_hello(request, name):
    return f'Hello {name}'


@app.route('/sum/{num01:d}/{num02:d}')
def sum_numbers(request, num01, num02):
    return f'{num01} + {num02} = {num01 + num02}'


@app.route('/book')
class BookResource(View):

    def get(self, request):
        return 'Books page'

    def post(self, request):
        return 'Endpoint to create a book'


def django_like_route(request):
    return 'I am a django like route'


app.add_route('/django', django_like_route)


@app.route('/template')
def template_handler(request):
    return app.template(
        'index.html',
        context={'name': 'Endymion', 'title': 'Endymion Framework'}
    )
