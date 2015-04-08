from gevent import pywsgi
from router import Router


class Application(object):
    def __init__(self, urlpatterns=None):
        self.router = Router()
        self.router.add(urlpatterns or [])

    def process(self, request, start_response):
        view = self.router.resolve(request)
        return view().dispatch(request, start_response)

    def start(self, port=8000):
        server = pywsgi.WSGIServer(('', port), self.process)
        server.serve_forever()
