#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent import pywsgi
import re
from collections import OrderedDict

from response import Response


class View(object):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def dispatch(self, request, start_response):
        method = request['REQUEST_METHOD'].lower()
        if method in self.http_method_names:
            handler = getattr(self, method)
        else:
            raise AttributeError("Method not allowed")
        return handler(request, start_response)


class Router(object):
    def __init__(self):
        self.routes = OrderedDict()

    def add(self, args):
        """
        Add pattern with view
        :param args: iterable
        """
        for pattern, view in args:
            self.routes[re.compile(pattern)] = view

    def resolve(self, request):
        """
        Yield view for request path
        :param request:
        """
        path = request['PATH_INFO'] or "/"
        for regex in self.routes.keys():
            if regex.match(path):
                return self.routes[regex]


class Application(object):
    def __init__(self, urlpatterns=None):
        self.router = Router()
        self.router.add(urlpatterns or [])

    def process(self, request, start_response):
        view = next(self.router.resolve(request))
        return view.dispatch(request, start_response)

    def start(self, port=8000):
        server = pywsgi.WSGIServer(('', port), self.process)
        server.serve_forever()


class Index(View):
    def get(self, request, start_response):
        response = Response()
        start_response(response.status, response.headers)
        yield '<h1>Test</h1>\n'


if __name__ == '__main__':
    urlpatterns = [
        ("/", Index)
    ]
    app = Application(urlpatterns)
    app.start()
