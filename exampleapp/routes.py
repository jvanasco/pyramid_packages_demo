import logging
log = logging.getLogger(__name__)


def includeme(config):

    ##
    ##	First our Routes & Views
    ##

    config.add_route("main", "/")

    config.add_route("account::sign_up", "/account/sign-up")
    config.add_route("account::login", "/account/login")
    config.add_route("account::login_automatic", "/account/login-automatic")
    config.add_route("account::logout", "/account/logout")
    config.add_route("account::home", "/account/home")
    config.add_route("account::index", "/account")
    config.add_route("account::facebook_authenticate","/account/facebook-authenticate")
    config.add_route("account::facebook_authenticate_oauth","/account/facebook-authenticate-oauth")

    config.add_route("api-internal::is_logged_in", "/api/internal/is-logged-in")
    config.add_route("api-internal::is_logged_in_callback", "/api/internal/is-logged-in-callback")

    # MAKE SURE TO SCAN
    config.scan("exampleapp.views")

    ##
    ##	Next our Handlers
    ##

    config.add_handler( "tests::" , "/tests/{action}", "exampleapp.handlers.tests.Tests" )

