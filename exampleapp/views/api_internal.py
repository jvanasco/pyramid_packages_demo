import logging
log = logging.getLogger(__name__)

from ..lib import handlers as _base
from ..lib import helpers as h
from pyramid.view import view_config


class ApiInternal(_base.HandlerApi):

    @view_config(renderer='json', route_name="api-internal::is_logged_in")
    def is_logged_in(self):
        rval= h.rval()
        rval['logged-in']= 1 if h.is_logged_in() else 0 
        return rval
        
    
    @view_config(renderer='jsonp', route_name="api-internal::is_logged_in_callback")
    def is_logged_in_callback(self):
        rval= h.rval()
        rval['logged-in']= 1 if h.is_logged_in() else 0 
        return rval
