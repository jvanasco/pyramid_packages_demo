import unittest
import pyramid.paster
from pyramid import testing
import paste
from paste.deploy.loadwsgi import appconfig
from webtest import TestApp

import os
here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, '../../', 'development.ini'))


from exampleapp import main


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass


class IntegrationTestBase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = main({}, **settings)
        #super(IntegrationTestBase, cls).setUpClass()

    def setUp(self):
        if 0:
            self.app = TestApp(self.app)
        elif 0:
            self.app = paste.deploy.config.PrefixMiddleware(self.app)
        elif 1:
            self.app = TestApp(pyramid.paster.get_app('development.ini#main'))
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()


class TestViews(IntegrationTestBase):
    pass


cookie_preview= 'ea_preview=1234567890'

def headers_preview():
   return { "Cookie" : cookie_preview , 'REMOTE_ADDR':'127.0.0.1' }

def headers_https():
   return { "HTTP_X_FORWARDED_SCHEME" : 'https', "HTTP_X_FORWARDED_PROTO" : 'https', 'wsgi.url_scheme': 'https', 'REMOTE_ADDR':'127.0.0.1' }

def headers_util( headers=None , is_preview=False, is_https=False):
    if headers == None:
        headers = {}
    if is_preview :
        headers.update( headers_preview() )
    if is_https :
        headers.update( headers_https() )
    return headers
