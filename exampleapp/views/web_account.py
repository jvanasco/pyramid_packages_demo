import logging
log = logging.getLogger(__name__)

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response


import datetime
from facebook_utils import FacebookPyramid
import pyramid_formencode_classic as formhandling

from ..lib import handlers as _base
from ..lib import helpers as h
from ..lib import forms

class WebAccount(_base.Handler):


    def __new_fb_object(self):
        """helper function, just creates a new facebook object"""
        oauth_code_redirect_uri= self.request.registry.settings['facebook.app.oauth_code_redirect_uri']
        fb= FacebookPyramid( self.request , oauth_code_redirect_uri=oauth_code_redirect_uri )
        return fb
        
        
    def __new_user(self):
        return h.Useraccount(id=1,name='sample user')

    @h.require_logged_out
    @view_config(route_name="account::sign_up")
    def sign_up(self):
        log.debug('web_account.py::sign_up')
        self.request.nav_section.signup= True
        if 'submit' in self.request.POST:
            return self._sign_up_submit()
        return self._sign_up_print()

    def _sign_up_print(self):
        log.debug('web_account.py::_sign_up_print')
        fb= self.__new_fb_object()
        return render_to_response( "web/account/sign_up.mako" , {"project":"ExampleApp",'fb':fb  } , self.request) 

    def _sign_up_submit(self):
        log.debug('web_account.py::_sign_up_submit')
        try:
            ( result , formStash ) = formhandling.form_validate( self.request , schema=forms.FormSignup , error_main="There was an error with your form.")
            if not result :
               raise formhandling.FormInvalid()
            
            useraccountInstance= self.__new_user()
            h.do_login( self.request , useraccount=useraccountInstance  , login_type='signup' )
            return HTTPFound(location='/account/home')

        except formhandling.FormInvalid:
            return formhandling.form_reprint( self.request , self._sign_up_print )
            
        except :
            raise



    @view_config(route_name="account::index")
    def index(self):
        log.debug('web_account.py::index')
        if h.is_logged_in():
            return HTTPFound(location='/account/home')
        return HTTPFound(location='/account/sign-up')



    @h.require_logged_out
    @view_config(route_name="account::login")
    def login(self):
        log.debug('web_account.py::login')
        self.request.nav_section.login= True
        if 'login' in self.request.POST:
            h.gaq_setCustomVar(1,'pagetype','login-submitted')
            return self._login_submit()
        h.gaq_setCustomVar(1,'pagetype','login-firstview')
        return self._login_print()


    def _login_print(self):
        log.debug('web_account.py::_login_print')
        self.request.pyramid_opengraph_item.set('og:title','Login to MyApp')
        self.request.pyramid_opengraph_item.set('og:description','This is the login page')
        fb= self.__new_fb_object()
        return render_to_response( "web/account/login.mako" , {"project":"ExampleApp",'fb':fb  } , self.request) 


    def _login_submit(self):
        log.debug('web_account.py::_login_submit')
        
        try:
            ( result , formStash ) = formhandling.form_validate( self.request , schema=forms.FormLogin , error_main="There was a problem with your form" )
            if not result:
               raise formhandling.FormInvalid()
               
            form_wrapper= formhandling.get_form(self.request)
            if ( form_wrapper.results['email_address'] != "user@domain.com" ) or ( form_wrapper.results['password'] != "password" ) :
                formhandling.formerrors_set( self.request , section='Error_Main' , message='that is not a valid account')
                raise formhandling.FormInvalid()
                
            useraccountInstance= self.__new_user()
            h.do_login( self.request , formStash.results['remember_me'] , useraccount=useraccountInstance , login_type="login")
            return HTTPFound(location='/account/home')

        except formhandling.FormInvalid:
            return formhandling.form_reprint( self.request , self._login_print )




    @h.require_logged_in
    @view_config(route_name="account::logout")
    def logout(self):
        log.debug('web_account.py::logout')
        h.do_logout( self.request )
        return HTTPFound(location='/')


    @h.require_logged_in
    @view_config(route_name="account::home")
    def home(self):
        log.debug('web_account.py::home')
        self.request.nav_section.dashboard= True
        return render_to_response( "web/account/home.mako" , {"project":"ExampleApp"} , self.request) 

        
        
    def _facebook_ensure_account_import( self , access_token , profile ):
        """ consolidate the account import stuff. this is because facebook will "login" and not "signup" someone who has already granted on their side, but we may be obvilious to ( closed connections, server failures, etc ).  raise a ValueError if we can't import
        """
        if not profile or not access_token:
            return HTTPFound(location='/account/sign-up?error=facebook-oauth-failure')
        
        if not profile['email']:
            raise ValueError('Missing Email')

        # have you seen this facebook user before?
        facebookAccount= 0 # query the database
        if not facebookAccount:
            pass
            # we're not doing any persistance, this is just to show you

        # do you have an account for the facebook user? 
        useraccountInstance = 0 # query the database for an existing user of that facebook id
        if not useraccountInstance:
            pass
            # create the user

        # if you don't have an exisitng user, then create a new one
        if not useraccountInstance:
            pass
            # create the user here


    @view_config(route_name="account::facebook_authenticate")
    def facebook_authenticate(self):
        log.debug('web_account.py::facebook_authenticate')

        # prove that we are logged in as a user
        fb_access_token= self.request.params.get('accessToken')
        fb_signed_request= self.request.params.get('signedRequest')
        fb_user_id= self.request.params.get('userID')
        
        fb= self.__new_fb_object()
        ( verified , payload ) = fb.verify_signed_request( signed_request=fb_signed_request , timeout=600 )
        if not verified :
            return HTTPFound(location='/account/login?error=FacebookAuthError')
            
        # query the user in the database by their facebook id
        useraccountInstance= 0 
        
        if useraccountInstance:
            # log them in
            log.debug('caught this user')
            useraccountInstance= self.__new_user()
            h.do_login( self.request , useraccount=useraccountInstance , login_type="facebook" )
            return HTTPFound(location='/account/home')

        else:
            # it's possible to catch some corrupted users here 
            access_token= None
            if 'accessToken' in self.request.GET:
                access_token = self.request.GET['accessToken']
                fb= self.__new_fb_object()
                profile= fb.graph__get_profile_for_access_token(access_token=access_token)
                self._facebook_ensure_account_import( access_token , profile )
                useraccountInstance= self.__new_user()
                h.do_login( self.request , useraccount=useraccountInstance , login_type="facebook" )
                self.request.session['facebook_profile']= profile
                return HTTPFound(location='/account/home')
                
        # catch the other folks here
                
        return HTTPFound(location='/account/signup?error=NEED TO SIGN UP AGAIN')
        
        
    @view_config(route_name="account::facebook_authenticate_oauth")
    def facebook_authenticate_oauth(self):
        log.debug('web_account.py::facebook_authenticate_oauth')
        fb= self.__new_fb_object()
        access_token= fb.oauth_code__get_access_token()
        ( access_token , profile )= fb.oauth_code__get_access_token_and_profile()
        
        # we use a single tool to ensure an account import for signup & login
        self._facebook_ensure_account_import( access_token , profile )
        useraccountInstance= self.__new_user()
        h.do_login( self.request , useraccount=useraccountInstance  , login_type="facebook" )
        self.request.session['facebook_profile']= profile
        return HTTPFound(location='/account/home')


    @h.require_nothing
    @view_config(route_name="account::login_automatic")
    def login_automatic(self):
        log.debug('web_account.py::login_automatic')
        url = self.request.params.get('url')
        if not url:
            url= '/account/home'
        if self.request._app_meta.is_logged_in:
            raise HTTPFound(url)
        if h.COOKIENAME_AUTOLOGIN in self.request.cookies :
            encrypted= self.request.cookies[h.COOKIENAME_AUTOLOGIN].encode('ascii')
            try:
                payload= h.signing.encryptionFactory.decode( encrypted , hashtime=True )
                if payload:
                    database_useraccount_id = 1

                    if database_useraccount_id == 1:
                        log.debug("AutoLogin success")
                        useraccountInstance= self.__new_user()
                        h.do_login( self.request , useraccount=useraccountInstance , remember_me=False , login_type='autologin' )
                        raise HTTPFound(url)
            except:
                log.debug("AutoLogin failure")
                pass
        raise HTTPFound(url)

