from api import API


app = API()


@app.route('/')
def index(request, response):
    response.text = 'Hello from index page'


@app.route('/about')
def about(request, response):
    response.text = 'Hello from about page'
