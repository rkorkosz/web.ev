from collections import OrderedDict
import re


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
            reg = regex.match(path)
            import ipdb; ipdb.set_trace()
            if reg:
                return self.routes[regex]