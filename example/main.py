#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from jinja2 import Environment, FileSystemLoader
from webev.application import Application
from webev.views import View

env = Environment(loader=FileSystemLoader('./templates'))


class Index(View):
    def get(self, request):
        template = env.get_template('index.html')
        return template.render()


if __name__ == '__main__':
    urlpatterns = [
        ("/", Index),
        ("^.*/$", Index)
    ]
    app = Application(urlpatterns)
    app.start()
