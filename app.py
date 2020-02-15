from api import API


app = API()


@app.route('/')
def index(request, response):
    response.text = 'Hello from index page'


@app.route('/about')
def about(request, response):
    response.text = 'Hello from about page'


@app.route('/hello/{name}')
def say_hello(request, response, name):
    response.text = f'Hello {name}'
