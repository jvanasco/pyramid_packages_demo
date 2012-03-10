import logging
log = logging.getLogger(__name__)

from pyramid.view import view_config

from ..lib import handlers as _base

class MainHandler(_base.Handler):

    @view_config(renderer='web/index.mako', route_name="main")
    def index(self):
        log.debug("testing logging; entered MainHandler.index()")
        self.request.nav_section.splash= True
        self.request.pyramid_opengraph_item.set('og:title','Login to MyApp')
        self.request.pyramid_opengraph_item.set('og:description','This is the login page')
        return {'project':'exampleapp'}
