import pytest


def test_basic_route_adding(app):


def test_route_overlap_throws_exception(app):
    @app.route('/home')
    def index(request):
        return 'YOLO'

    assert '/home' in app.routes

    with pytest.raises(AssertionError):
        @app.route('/home')
        def index02(request):
            return 'YOLO'
