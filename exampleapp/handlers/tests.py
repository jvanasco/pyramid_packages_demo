import logging
log = logging.getLogger(__name__)

from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response

from ..lib import handlers as _base 

class Tests(_base.Handler):


    @action(renderer='/web/account/test1.mako')
    def test1(self): 
        """sample handler using @action decorator"""
        return {'project':'ExampleApp'}

    def test2(self):
        """sample handler using no decorator, and returning a render_to_response"""
        return render_to_response( "/web/account/test2.mako" , {"project":"ExampleApp"} , self.request ) 
