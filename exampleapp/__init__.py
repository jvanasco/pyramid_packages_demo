import logging
log = logging.getLogger(__name__)

from pyramid.config import Configurator
from pyramid.renderers import JSONP
import pyramid_beaker
from .subscribers import mongodb
import pyramid_subscribers_cookiexfer

from pyramid_subscribers_beaker_https_session import initialize_https_session_set_request_property


def url_transformer(method_name):
    """this is required when using pyramid handlers; it lets us map `/section/dash-in-name` to `dash_in_name` """
    return method_name.replace('_', '-')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    # i define a method_name_xformer in the handlers above. it simply turns /this-url into /this_url so we can have happier methods
    settings['pyramid_handlers.method_name_xformer'] = url_transformer

    config = Configurator(settings=settings)


    # Create the Pyramid Configurator.
    config = Configurator(settings=settings)
    config.include("pyramid_handlers")

    # Configure Beaker sessions and caching
    session_factory = pyramid_beaker.session_factory_from_settings(settings)
    config.set_session_factory(session_factory)
    pyramid_beaker.set_cache_regions_from_settings(settings)

    # Add in our session_https property ( see import above )
    initialize_https_session_set_request_property( config , settings )

    # Configure renderers
    config.add_renderer('jsonp', JSONP(param_name='callback'))


    # Set up views & handlers
    config.include("exampleapp.routes")

    ## add static view will mount the 'static' folder as a /static
    #config.add_static_view("static", "static", cache_max_age=int(settings['static.cache_max_age']))

    ## the akhet app provides for add_static_route working as an 'overlay', which i prefer
    ## this means that urls are viewed as /img/logo.png instead of /static/img/logo.png
    ## this is really only affected on the dev environment, as static files would be served by nginx on production
    config.include('akhet')
    ## make your caching dependent on the environment.ini
    config.add_static_route("exampleapp", "static", cache_max_age=int(settings['static.cache_max_age']))


    # initialize pyramid_subscribers_cookiexfer
    pyramid_subscribers_cookiexfer.initialize_subscribers( config , settings )

    # Initialize mongodb , which is a subscriber
    mongodb.initialize_mongo_db( config , settings )

    # get 'h' into the templates
    config.add_subscriber(\
        "exampleapp.subscribers.add_renderer_globals",
        "pyramid.events.BeforeRender")


    # Set up of views and handlers occurs in routes
    config.include("exampleapp.routes")


    return config.make_wsgi_app()
