import logging
log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_request

from gaq_hub.pyramid_helpers import *
from htmlmeta_hub.pyramid_helpers import *

from login_status import *


class AttributeSafeObject(object):
    """object, with lax attribute access ( returns '' when the attribute does not exist). From pylons."""
    
    def __init__(self,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
    
    def __getattr__(self, name):
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            log.debug("No attribute called %s found on AttributeSafeObject object, returning empty string", name)
            return ''


class NavSectionObject(object):
    """ Create an attribute for each 'nav section', 
    Set to "true" to enable it
    """
    dashboard= None
    login= None
    signup= None
    splash= None
    
    def __getattribute__( self, name ):
        try:
            if object.__getattribute__( self, name ):
                return '''class="active"'''
        except :
            pass
        return ''


class Useraccount(object):
    id= None
    name= None
    
    def __init__(self,id=None,name=None):
        self.id = id
        self.name = name


def rval():
    return { 'status':'error' }
    