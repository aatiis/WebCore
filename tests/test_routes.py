# encoding: utf-8

from common import PlainController, WebTestCase

import web.core
from web.core.dialects.routing import RoutingController
from web.core import Application, RESTMethod


class BarController(object):
    def error(self, foo):
        return "sub"

class RootController(RoutingController):
    def __init__(self):
        super(RootController, self).__init__()

        self._map.connect(None, '/error/{foo}', action="error")
        self._map.connect(None, '/error/{foo}/bar', controller="bar", action="error")

    bar = BarController()

    def error(self, foo):
        return repr(foo)


test_config = {'debug': True, 'web.widgets': False, 'web.sessions': False, 'web.compress': False, 'web.static': False}


class TestRESTfulDispatch(WebTestCase):
    app = Application.factory(root=RootController, **test_config)

    def test_basic(self):
        self.assertResponse('/', '404 Not Found', 'text/html')
        self.assertResponse('/error', '404 Not Found', 'text/html')
        self.assertResponse('/error/', '404 Not Found', 'text/html')
        self.assertResponse('/error/foo', '200 OK', 'text/html', body="u'foo'")
        self.assertResponse('/error/bar', '200 OK', 'text/html', body="u'bar'")
        self.assertResponse('/error/baz/bar', '200 OK', 'text/html', body="sub")
