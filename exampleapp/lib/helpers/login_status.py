import logging
log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPFound
from pyramid.threadlocal import get_current_request

from . import signing

COOKIENAME_AUTOLOGIN= 'autologin'
COOKIENAME_USERNAME= 'username'
COOKIENAME_LOGGEDIN = 'loggedin'





class LoginType(object):
    """We're not doing anything with this -- yet.  But anything sent to do_login should be recorded here"""
    autologin = 0
    lost_password= 0
    email_verification= 0
    login= 0
    signup= 0
    facebook= 0


def do_login( request, remember_me=False , login_type=None , useraccount=None ):
    """example of a login helper"""

    max_age= None
    if remember_me:
        max_age= 2592000

    request.session['logged_in']= True
    request.response.set_cookie( COOKIENAME_LOGGEDIN, value='1', max_age=max_age, path='/' )
    request.response.set_cookie( COOKIENAME_USERNAME, value=useraccount.name, max_age=max_age, path='/' )

    if remember_me:
        payload = { 'useraccount_id': useraccount.id }
        payload = signing.encryptionFactory.encode( payload , hashtime=True )
        request.response.set_cookie( COOKIENAME_AUTOLOGIN, value=payload, max_age=max_age, path='/' )


def do_logout(request):
    """example of a logout helper"""
    request.session.invalidate()
    request.response.set_cookie( COOKIENAME_AUTOLOGIN, value='1', max_age=0, path='/' )
    request.response.set_cookie( COOKIENAME_LOGGEDIN, value='1', max_age=0, path='/' )
    request.response.set_cookie( COOKIENAME_USERNAME, value='1', max_age=0, path='/' )
            

def is_logged_in(request=None):
    """example of a status check"""
    if request is None:
        request= get_current_request()
    if not request.session:
        return False
    if 'logged_in' in request.session and request.session['logged_in']:
        return request.session['logged_in']
    return False



def require_logged_in(wrapped):
    """example of a decorator to require is_logged_in()"""
    log.debug("helpers.__init__.py -- require_logged_in()")
    def wrapper(self, *arg, **kw):
        log.debug("helpers.__init__.py -- require_logged_in().wrapper")
        try:
            if not is_logged_in(self.request):
                log.debug("require_logged_in ; redirecting to /account/login")
                result= HTTPFound(location='/account/login')
            else:
                result = wrapped(self, *arg, **kw)
        finally:
            pass
        return result
    wrapper.__name__ = wrapped.__name__
    wrapper.__doc__ = wrapped.__doc__
    wrapper.__docobj__ = wrapped # for sphinx
    return wrapper



def require_logged_out(wrapped):
    """example of a decorator to require a false is_logged_in()"""
    log.debug("helpers.__init__.py -- require_logged_out()")
    def wrapper(self, *arg, **kw):
        log.debug("helpers.__init__.py -- require_logged_out().wrapper()")
        try:
            if is_logged_in(self.request):
                log.debug("require_logged_out ; redirecting to /account/home")
                result= HTTPFound(location='/account/home')
            else:
                result = wrapped(self, *arg, **kw)
        finally:
            pass
        return result
    wrapper.__name__ = wrapped.__name__
    wrapper.__doc__ = wrapped.__doc__
    wrapper.__docobj__ = wrapped # for sphinx
    return wrapper




def require_nothing(wrapped):
    log.debug("helpers.login_status.py -- require_nothing()")
    def wrapper(self, *arg, **kw):
        log.debug("helpers.login_status.py -- require_nothing().wrapper()")
        return wrapped(self, *arg, **kw)
    wrapper.__name__ = wrapped.__name__
    wrapper.__doc__ = wrapped.__doc__
    wrapper.__docobj__ = wrapped # for sphinx
    return wrapper

