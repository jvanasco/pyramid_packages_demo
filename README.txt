# ExampleApp README

This is a quick howto explaining a few pyramid extensions I made, and showing how I like to set up projects.

The packages i'm illustrating :

* gaq_hub - python interface to generating Google Analytics javascript. pyramid helpers to ease integration into your apps.
* htmlmeta_hub - helpers & objects to provide a simple stash to store document meta information
* opengraph_writer - lightweight opengraph metadata validation and generation
* facebook_utils - generates and validates oAuth flow with Facebook.com
* pyramid_subscribers_cookiexfer - subscribers to automate persisting cookies throughout redirects in pyramid
* pyramid_formencode_classic - formencode parsing library to emulate (and improve upon) the original pylons validation mechanisms
* pyramid_subscribers_beaker_https_session - supports an ancillary https only cookie/session
* insecure_but_secure_enough - cryptography that is good enough for non-sensitive information , like an autologin

This is also a crash-course on setting up a pyramid app with a bunch of Web 2.0 stuff, using the pyramid_handlers dispatch system.

Buzzwordy things this uses:

* pyramid
* jquery
* 960.gs
* facebook connect / login
* facebook open graph
* google analytics
* mongodb

jquery is included in this, and is distributed under the MIT or GPL license. your choice. [ http://jquery.org/license/ ]

960.gs is included in this, and is distributed under the MIT or GPL license. your choice. [ http://960.gs/ ]

the code of this example is released under the MIT license [http://www.opensource.org/licenses/mit-license.php]
the docs/tutorial are released under the Creative Commons Attribution-ShareAlike license [ http://creativecommons.org/licenses/by-sa/3.0/ ]


There are extensive calls to log.debug() and inline comments to show how everything fits together.


# Instant Gratification

1. Clone this
2. `cd` into the directory, then `python setup.py develop` ( preferably from a virtualenv

The information below gives an overview on how the app was built, and how all the components are configured and fit together.


# Organize the project

I like to organize my workspace up like this:

* ~/work/projects/APPLICATION_NAME
**	a revision controlled repository for the application. it contains both the documentation, production work, and the application.  i typically have the pyramid/pylons apps within an "apps" subdirectory.  Sometimes a project has more than one "app" in it.

* ~/work/environments/APPLICATION-PYTHON_VERISION
** a bunch of python virtual environments, one per project

* ~/go_APPLICATION.source
** a "source file" that puts me into the virtualenv and project path immediately.  it typically looks like this:

    cd ~/work/projects/PROJECT/apps/APPLICATION
    source ~/work/environments/APPLICATION-PYTHON_VERISION/bin/activate

I also like to organize the file structure a bit differently too.

* my "static" directories tend to have /js /css /img  ; sometimes i have them as /_js /_css /_img so they sort nicely

* i prefer having python top-level package files named feature/__init__.py rather than feature.py -- i always find myself extending things

* i like to preface my handlers with web_ and mobile_ ; and have /web and /mobile toplevel directories.  some people like having the same feature in the same package, but in my usage i tend to have different user experiences across platforms and I find it easier to divide work across team members and manage a merge process

* i like to use partials and template inheritance.  anything that should never be rendered itself ( like a site template or a footer file ) i pre-pend with an @ sign.  The @sign is not RFC valid for a url part, so could never use used as a static file or view name 

* i like to keep forms in a separate module.  i find that i re-use them more often when they're nice and consolidated.


# ok, let's get going...



very quickly...

	$ mkdir -p ~/work/projects/PyramidExamples/apps
	$ mkdir -p ~/work/environments
	$ cd ~/work/environments
	$ virtualenv PyramidExamples_ExampleApp-2.7
	$ vi ~/go_PyramidExamples_ExampleApp.source
	
and then edit the file into...

    source ~/work/environments/PyramidExamples_ExampleApp-2.7/bin/activate
    cd ~/work/projects/PyramidExamples/apps/ExampleApp

to jump into the environment i just do...

	$ source ~/go_PyramidExamples_ExampleApp.source

before i do that though, i'd want to manually do this:

    # activate the environment
    $ source ~/work/environments/PyramidExamples_ExampleApp-2.7/bin/activate
    
    # jump into the folder
    $ cd ~/work/projects/PyramidExamples/apps
    
    # make the scaffold
    $ pcreate -t starter ExampleApp


IIRC, if you have pyramid on the core python install pcreate will be available.  If its not, just "pip install pyramid".

I like to use a modified version of Mike Orr's akhet scaffold.  I used the "starter" template as I didn't want to include any persistance (for ease of examples), and just customized it.

	$ cd ~/work/projects/PyramidExamples/apps/ExampleApp/exampleapp
	$ mkdir handlers
	$ touch handlers/__init__.py
	$ mkdir subscribers
	$ touch subscribers/__init__.py
	$ mkdir -p lib/helpers
	$ touch lib/__init__.py
	$ touch lib/helpers/__init__.py

now that the structure is finished, i'll jump to the root of the app and edit the requirements

	$ cd ~/work/projects/PyramidExamples/apps/ExampleApp
	$ vi setup.py

I want to add pyramid_handlers  , which makes the environment pylons-like.  i personally prefer it.

Next I'll add a handful of modules I open sourced:

	* gaq_hub - centrally manages google analytics
	* htmlmeta_hub - centrally manages metadata for documents
	* opengraph_writer - centrally manages facebook open graph metadata, provides some simple validation and debugging
	* facebook_utils - simplifies authenticated logins with facebook
	* pyramid_subscribers_cookiexfer - helps manage setcookie on redirects
	* pyramid_formencode_classic - provides some formhandling routines that I found useful under pyramid
	* pyramid_subscribers_beaker_https_session - supports an ancillary https only cookie/session
	* insecure_but_secure_enough - cryptography that is good enough for non-sensitive information , like an autologin

Finally, we'll install the app into the development path, which will also install all the modules we need... 

	$ python setup.py develop

If you wanted to test the scaffold now...

	$ pserve development.ini

Running? Great.  Cancel and let's continue...

I want to edit the development.ini with some values:

I like to set an "app domain" per environment.  I find this to be really helpful when integrating against social sharing sites, etc.

	app_domain = http://127.0.0.1:6543

i also like to set a cache_max_age in the environment too:

	static.cache_max_age = 10
	
The default scaffolds hardcode this, but I find that a LONG cache is good on production while nearly no caching is optimal for development ( as you often change javascript within seconds )



## MongoDB Integration ( pyramid_mongodb )

Niall O'Higgins created the pyramid_mongodb package as an application scaffold.

I forked the package and extended his idiom to work as a subscriber, so the package becomes more re-usable. He's merged it into the github repo, but its not in pypi yet, so we'll manually create the subscriber for now.


In any event, edit your development.ini as follows

	mongodb_use = false
	mongodb_uri = mongodb://localhost
	mongodb_name = exampleapp

note that we're setting it to being OFF.  I don't want to be running mongo just yet, and the subscriber will FAIL the startup process if it can't connect.  So let's just leave it off.


## Cookie Transfer Integration  ( pyramid_subscribers_cookiexfer )


I wrote a small subscriber to migrate cookies out of redirects, and either save them to the session ( and set them on the next visit) or push them to the browser immediately ( which works for everyone but safari ).

Full docs about how this works and we it's needed are here: https://github.com/jvanasco/pyramid_subscribers_cookiexfer

For simplicity, we're just going to enable everything, and 'eliminate' a few directories from being covered by the package ( this way we have cleaner debug statements )

	cookie_xfer.redirect_add_headers = True
	cookie_xfer.redirect_add_headers__unique = True
	cookie_xfer.redirect_session_save = True
	cookie_xfer.redirect_session_save__unique = True
	cookie_xfer.re_excludes = "^/(css|img|js|deform|_debug_toolbar)"

## Google Analytics Integration  ( gaq_hub )

You'll need to do the following steps:

1. Create an account with google analytics, if you don't have one already.
2. Create a PROPERTY on google analytics for your site / project
3. Create TWO tracking codes / suites in that property.  One if for public, one is for development.

Your tracking codes should look like this , and you should name the suites "DEVELOPMENT" and "PRODUCTION".  You might even have staging, etc.

	UA-00000000-1
	UA-00000000-2

In your environment.ini, you'll want to add this line:

	gaq.account_id= UA-00000000-1


## Facebook Integration ( facebook_utils )

You should create TWO applications on Facebook.  One for public use, the other for developer use.

### MyApp-Dev

Developer testing app.  use the id/secret values from it for "development.ini"

#### Basic Page - "Basic Info" Section

- Name: MyApp-Dev
- App Domain: can be blank

#### Basic Page - "Select How your app integrates with Facebook" Section

- Site URL : test URL ( for me, this is "http://127.0.0.1:6543" , the port MUST match your app's port on localhost.  if your app is running on a virtualhost )

#### Advanced Tab - "Authentication"

- Select Sandbox Mode

### MyApp

Production app.  use the id/secret values from it for "production.ini"

#### Basic Page - "Basic Info" Section

- Name: MyApp
- App Domain: production Domain , i.e. "ExampleApp.com"

#### Basic Page - "Select How your app integrates with Facebook" Section

- Site URL : production URL , i.e. "http://ExampleApp.com"

#### Advanced Tab - "Authentication"

- Select Sandbox Mode.  Deselect it when you want to go public.


### Setting your environment.ini variables

The following lines should go in your development.ini
	
	facebook.app.id= %(facebook_app_id)s
	facebook.app.secret= %(facebook_app_secret)s
	facebook.app.scope= email
	facebook.app.oauth_code_redirect_uri= http://127.0.0.1:6543/account/facebook-authenticate-oauth?response_type=code

You'll want to specify exactly what your app's id, secret, and scope are.

Right now you can specify them on the commandline 

	pserve --reload development.ini facebook_app_id=123 facebook_app_secret=123456

The app will not start without these arguments (real or fake) being passed in.  You can just substitute real or fake values into the development.ini file so you can more easily start the server with..

	pserve --reload development.ini

It's important to note here that whatever you configure Facebook to recognize must be the exact same environment as your app.

For example , if you tell facebook that your app is on 127.0.0.1:5000  , then requests to facebook MUST originate from that ( facebook's javascript library knows ).  Your app might still work on 0.0.0.0:5000 , but that will break Facebook.  Similarly, using a different port will require re-configuring facebook -- so if you decide to start testing https sessions and set up nginx to run on 127.0.0.1 ( implicit port 80), Facebook must be configured to expect that as well.
	
	
I've provided a stub of Facebook JSSDK integration in /static/js/web.js

There's a detailed explanation on my blog here: http://www.destructuring.net/2011/12/08/facebook-developer-notes-javascript-sdk-and-asynchronous-woes/

A few things you should note about this integration:

0. This integration is just a very simplified tutorial / explanation to get you started.	

1. we initialize our facebook integration by dropping the facebook sdk code in the site-template AND THEN making a call to the fbUtils.initialize() which is defined our file js/web.js

2. the templates/web/account/login.mako file contains this line:
	fbUtils.ensureInit(fbUtils.login_page_facebook_init);
	
	fbUtils.ensureInit is a helper function that uses javascript setIntervals to ensure that we're connected to facebook before something runs.  this makes us bug-free in terms of load-order
	
	`login_page_facebook_init` checks to see if we're logged in.  if we are, it redirects the user to /account/facebook-authenticate , which will log the user in via the Facebook API. 
	
	As long as you are logged-in to facebook and opted-in to your facebook app , this redirect will occur.  You'll have to opt-out of your facebook app a lot during testing. 

3. The signup page has similar features to the login page.

4. If you do an initial sign up, you'll be redirected to /account/facebook-authenticate-oauth , which has a different server-side flow



	
	
# Configure the app's __init__.py

exampleapp/__init__.py is the master bit of 'setup' code for your app.  

I'd suggest looking at the setup in detail, but a quick overview is this:

    # make your caching dependent on the environment.ini
    config.add_static_route("static", "static", cache_max_age=int(settings['static.cache_max_age']))

    # initialize pyramid_subscribers_cookiexfer
    import pyramid_subscribers_cookiexfer
    pyramid_subscribers_cookiexfer.initialize_subscribers( config , settings )

    # Initialize mongodb , which is a subscriber
    from .subscribers import mongodb
    mongodb.initialize_mongo_db( config , settings )

    # Add in our session_https property ( see import above )
    initialize_https_session_set_request_property( config , settings )

    # Set up views & handlers
    config.include("exampleapp.routes")

Take a look at the subscribers/mongodb.py file to quickly see how that works.

Also look at routes.py to see how I configured all the routes , added handlers, and scanned for views.


# Create a base handler

check out exampleapp/lib/handlers.py

in there, i define a base handler that does a few key things:

1. I attach 'request' to self.request
2. I call h.htmlmeta_setup(), which is a helper function from htmlmeta_hub imported into the helpers package.  this initializes the core htmlmeta item and attaches it to the request. ( htmlmeta_hub )
3. I put an _app_meta object on the request.  it's just a stash of random data that I tend to need.  notice how I put login status there - this way i don't continually call a helper function (even if it is simple). I also have a 'facebook_enable' flag - if i only want the facebook SDK loaded on certain pages, my templates will control loading it via that.
4. I initialize an opengraph item for the page , provided by pyramid_opengraph_item , using some site defaults which I will override later ( opengraph_writer )
5. I make a call to gaq_setup, another function imported into the helpers package  ( gaq_hub )
6. I attach a lib.helpers.NavSectionObject() to the request.  This is a little object where I stash the current "nav element" within my views.  In the site-template, I can quickly check to see if I'm on the current nav section and print "class='active'".  There are a lot of mechanisms to handle this sort of need, I found this to be very easy and fairly lightweight.


# Create logical handlers...

I've shown a handful of ways to make 'logical handlers' - both in the /app/handlers and /app/views directories

Note that I've chosen not to use Pyramid's security system, and opted to use a custom decorator based authentication system.  methods are decorated as @require_logged_in and @require_logged_out , which are controlled via helper functions.

I chose to do this only because it was faster to get a system based on this method ported from Pylons code to Pyramid on one of my projects [than it would be to build something new onto the Pyramid auth scheme] -- and this is simpler to illustrate here than the pyramid auth options.


# form handling with pyramid_formencode_classic

The easiest way to see how I approach formhandling is within /views/web_account.py and the login routine

I provide an executable view on `def login(self)`.  

This function then dispatches the login logic as follows:

• If it looks like we're submitting a form, call self._login_submit() , otherwise call self._login_print() to print the form
• Everything within _login_submit() is encapsulated in a try/except block.  If we can't login, set the appropriate errors for rendering, and then re-render the form using _login_print.

I also like to consolidate all the forms in /lib/forms.py - I find that is better for re-use and keeping naming conventions standard across form fields.



# encrypting cookies with insecure_but_secure_enough

Again look at the login function.  if we have a successful login attempt, we call /lib/helpers::login() and pass in whether or not we have a "remember_me" election.

If the user wants to be remembered, we do two things:
• We set the max_age on cookies to be 30 days
• We create a "payload" that is a dict which merely includes the user's id , and encrypt it.
• We set an autologin cookie with that payload.

NOTE - this should ONLY be done over a secure https channel.  

Looking at our lib/handlers.py file, you'll see on our Handler class that if we're not logged in but have an autologin cookie, we redirect to /account/login-automatic

login-automatic simply tries to decrypt the cookie and log the user in.

cryptography occurs via a factory registered in /lib/helpers/signing.py

The factory is configured with an RSA key , and miscellaneous secrets used to seed for encryption and signing.

The insecure_but_secure_enough offers a multi-stage clearance for encrypted cookies-- they have a time-based hmac expiry for lightweight validation , which must be cleared before you decrypt.  This was designed to both reduce the overhead of decrypting cookies only to find out they're too old, and also allowing the ability to set up a factory that provides different signing credentials for every day of the year.

You can sign pretty much anything you want, just know that there is a 4k limit.  I used a 1024 bit key, but you could do 2048 easily.

The library simply encrypts/decrypts data , and allows for checksums -- so you could use this to handle autologin URLs or similar.

Finally, note that in the do_login() helper function , I've attached a login_type argument. You should be in the habit of noting HOW someone logged in -- depending on what your app does, you may not want only allow those who have manually logged in to access account-information, and force an auto-login to manually re-authenticate for sensitive operations.


# using secure sessions ( pyramid_subscribers_beaker_https_session )

This is a todo, as it is the most complex thing to illustrate.

Step 1 - You'll need to set up nginx ( or similar ) on your local machine , and then proxy-pass https traffic to your pyramid app ; or run pyramid on an https only mode.  I found the easiest thing to do is just run pyramid on port 5000 and then proxy http(80) and https(443) to it.

Step 2 - __init__.py has 2 relevant lines

	from pyramid_subscribers_beaker_https_session import initialize_https_session_set_request_property
	initialize_https_session_set_request_property( config , settings )
	
This will allow anything with session_https. or beaker_session_https. in your development.ini file to specify the https session cookie information.

the https session cookie will be an attribute of the request, as request.session_https.  

Please note -- on the first version of the package, it will be an empty session on non-https connections, version 0.0.2 and above will return NONE unless we're on an HTTPS session


# illustrating an https session via a load-balancer/upstream proxy , with nginx

The simplest way to simulate a production environment is to install nginx onto your local machine ( nginx.net )

Nginx is a super-small , very-lightweight webserver that many people prefer to run as the frontend proxy on their installations.

when you compile nginx, make sure you have the ssl module installed.

## create a key
i included a self-signed key in the ssl/ directory.

create the key + certificate signing request

	openssl req -new -nodes -keyout ssl.key -out ssl.csr

sign the csr into a cert

	openssl x509 -req -days 365 -in ssl.csr -signkey ssl.key -out ssl.crt

## configure nginx to use the key

i included a stripped-down verison of the config file for nginx  , which references the certs

## configure the app to use PasteDeploy's prefix middleware

prefix-middleware does a lot of things that we don't necessarily need.  it also does one thing we do need - adjust the environment vars to allow for https detection and various other proxy needs.  check out the 3 lines in development.ini used to configure this:

[app:main]
+filter-with = proxy-prefix

+[filter:proxy-prefix]
+use = egg:PasteDeploy#prefix

as of version 0.0.2 of my session_https module, the session will either be a session object on https connections, or None on http connections















# A GROWING TODO

1. Illustrate session & session_https differences , and lock session_https down more
2. 

