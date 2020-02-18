from endymion import exceptions


class View(object):

    def __call__(self, request, **kwargs):
        handler = getattr(self, request.method.lower(), None)

        if handler is None:
            raise exceptions.MethodNotAllowed()

        return handler(request, **kwargs)
