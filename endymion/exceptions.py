class EndymionBaseException(Exception):
    msg = 'Endymion Base Exception'

    def __init__(self, status_code=None, original_exception=None):
        super(EndymionBaseException, self).__init__()

        if status_code is not None and isinstance(status_code, int):
            self.status_code = status_code

        self.original_exception = original_exception


class HTTPError(EndymionBaseException):
    status_code = 500


class NotFound(HTTPError):
    msg = 'Not found.'
    status_code = 404


class InternalServerError(HTTPError):
    msg = 'An internal error happened.'


class RouteAlreadyExists(EndymionBaseException):
    msg = 'Such route already exists'


class MethodNotAllowed(EndymionBaseException):
    msg = 'Method not allowed'
