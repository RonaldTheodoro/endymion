class View(object):

    def __call__(self, request, **kwargs):
        handler = getattr(self, request.method.lower())

        if handler is None:
            raise AttributeError('Method not allowed', request.method)
        
        return handler(request, **kwargs)