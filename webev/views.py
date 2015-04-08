from webev.response import Response


class View(object):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dispatch(self, request, start_response, **kwargs):
        method = request['REQUEST_METHOD'].lower()
        if method in self.http_method_names:
            handler = getattr(self, method)
        else:
            raise AttributeError("Method not allowed")
        response = Response(**kwargs)
        start_response(response.status, response.headers)
        yield str(handler(request))
