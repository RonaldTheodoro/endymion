import webob


class API(object):

    def __call__(self, environ, start_response):
        request = webob.Request(environ)

        response = webob.Response()
        response.text = 'Hello World'

        return response(environ, start_response)
