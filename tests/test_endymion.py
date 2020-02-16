
def test_basic_route_adding(app):
    @app.route('/')
    def index(request):
        return 'YOLO'

    assert '/' in app.routes