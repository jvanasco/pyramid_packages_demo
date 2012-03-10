"""Base classes for view handlers.
"""
import logging
log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPFound

from ..lib import helpers as h

import datetime
import time

from opengraph_writer import pyramid_opengraph_item


class _CoreHandler(object):
    """All my handlers inherit from CoreHandler; this allows me to stash commonly needed functions"""
    pass


class Handler(_CoreHandler):

    def __init__(self, request):
        log.debug( "-----------------------------------------" )
        log.debug( "New Request -- Handler" )
        log.debug( "Path - %s " % request.environ['PATH_INFO'] )
        log.debug( "Params - %s " % request.params )
        log.debug( "Cookies - %s " % request.cookies )
        
        # stash the request as an attribute of the instance
        self.request = request

        # compute if we're logged in
        is_logged_in= h.is_logged_in(request), 

        # if we're not logged in BUT we have an autologin cookie, we can redirect to a login
        if not is_logged_in:
            if h.COOKIENAME_AUTOLOGIN in self.request.cookies :
                url = '/account/login-automatic'
                if self.request.environ['PATH_INFO'] != url :
                    log.debug("AutoLogin ; redirect")
                    raise HTTPFound(url)

        # i find it useful to create an _app_meta object that has some various info in it...
        self.request._app_meta= h.AttributeSafeObject(\
            is_logged_in= is_logged_in, 
            facebook_enable= True, 
            facebook_app_id= request.registry.settings['facebook.app.id'], 
            time= time.time() , 
            datetime= datetime.datetime.now(),
            app_domain= request.registry.settings['app_domain'], 
            app_domain_secure= request.registry.settings['app_domain_secure'], 
        )

        # i think a NavSectionObject makes it easier to control what element of the nav is 'active'
        self.request.nav_section= h.NavSectionObject()

        # initialize htmlmeta info for the app here, then upgrade it throughtout the request
        # it is finally printed out on @site-template.mako
        h.htmlmeta_setup(\
            request=request,
            title="ExampleApp.com", 
            description="awesome", 
            keywords="fun!",
        )

        # a pyramid_opengraph_item is the same thing as htmlmeta, but tailored to OpenGraph metadta
        og= pyramid_opengraph_item(request)
        og.set('og:type','website')
        og.set('og:site_name','ExampleApp')
        og.set('og:title','ExampleApp Page')
        og.set('og:description','ExampleApp is FUN')
        og.set('og:image','/img/og.png')
        
        # initialize google analytics support
        h.gaq_setup( request.registry.settings['gaq.account_id'] , request=self.request )



class HandlerApi(_CoreHandler):
    def __init__(self, request):
        log.debug( "-----------------------------------------" )
        log.debug( "New Request -- HandlerApi" )
        log.debug( "New HandlerApi Request -- init" )
        log.debug( "Path - %s " % request.environ['PATH_INFO'] )
        log.debug( "Params - %s " % request.params )
        log.debug( "Cookies - %s " % request.cookies )

        # stash the request as an attribute of the instance
        self.request = request

        # compute if we're logged in
        is_logged_in= h.is_logged_in(request), 

        self.request._app_meta= h.AttributeSafeObject(\
            is_logged_in= is_logged_in, 
            time= time.time() , 
            datetime= datetime.datetime.now(),
            app_domain= request.registry.settings['app_domain'], 
            app_domain_secure= request.registry.settings['app_domain_secure'], 
        )