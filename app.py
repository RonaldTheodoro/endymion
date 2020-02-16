from endymion import Endymion
from endymion.views import View


app = Endymion()


@app.route('/')
def index(request, response):
    response.text = 'Hello from index page'


@app.route('/about')
def about(request, response):
    response.text = 'Hello from about page'


@app.route('/hello/{name}')
def say_hello(request, response, name):
    response.text = f'Hello {name}'


@app.route('/sum/{num01:d}/{num02:d}')
def sum_numbers(request, response, num01, num02):
    response.text = f'{num01} + {num02} = {num01 + num02}'


@app.route('/book')
class BookResource(View):

    def get(self, request, response):
        response.text = 'Books page'

    def post(self, request, response):
        response.text = 'Endpoint to create a book'
