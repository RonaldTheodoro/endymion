class EndymionBaseException(Exception):
    msg = 'Endymion Base Exception'
    status_code = 500

    def __init__(self, status_code=None, original_exception=None):
        super(EndymionBaseException, self).__init__()

        if status_code is not None and isinstance(status_code, int):
            self.status_code = status_code

        self.original_exception = original_exception


class NotFound(EndymionBaseException):
    msg = 'Not found.'
    status_code = 404


class InternalServerError(EndymionBaseException):
    msg = 'An internal error happened.'
