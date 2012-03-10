<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en" xmlns:og="http://opengraphprotocol.org/schema/" xmlns:fb="http://www.facebook.com/2008/fbml">
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    
        ## htmlmeta is initialized on /lib/handlers.py , then upgraded throughout the request processing 
        <title>${h.htmlmeta_get('title',request=request)|n}</title>
        ${h.htmlmeta_as_html(request=request)|n}

        ## google analytics data is initialized on /lib/handlers.py , then upgraded throughout the request processing 
        ${h.gaq_as_html(request=request)|n}

        ## opengraph data is initialized on /lib/handlers.py , then upgraded throughout the request processing 
        ${request.pyramid_opengraph_item.as_html()|n}

        <script type="text/javascript" language="javascript" src="/js/jquery-1.7.min.js"></script>
        <script type="text/javascript" language="javascript" src="/js/web.js"></script>

        <link rel="stylesheet" href="/css/960.gs/reset.css" />
        <link rel="stylesheet" href="/css/960.gs/text.css" />
        <link rel="stylesheet" href="/css/960.gs/960.css" />
        <link rel="stylesheet" href="/css/web.css" />

    </head>
    <body>
        <div id="fb-root"></div>
        <script>
            window.fbAsyncInit = function() {
                ## lines that begin with two hashes (##) aren't rendered by mako 
                ## this FB.init call could be moved into the FS_Web_fbUtils code
                FB.init({
                    appId      : ${request._app_meta.facebook_app_id},
                    channelUrl : '//${request._app_meta.app_domain}/facebook-channel.html',
                    status     : true, 
                    cookie     : true,
                    xfbml      : true,
                    ## if oauth is set to true, will generate errors on login due to the js-sdk
                    oauth      : true 
                });

                ## wrap all our facebook init stuff within a function that runs post async, but is cached across the site
                fbUtils.initialize();
            };
            (function(d){
               var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
               js = d.createElement('script'); js.id = id; js.async = true;
               js.src = "//connect.facebook.net/en_US/all.js";
               d.getElementsByTagName('head')[0].appendChild(js);
             }(document));          
        </script>
        <header>
            <div class="container_12">
                <div class="grid_12">
                    <div id="nav">
                        ##
                        ## when i start a project out, i like to base the login status in the templates
                        ## as the project progresses, the visibility of everything will be controlled by css
                        ## at that point, i prefer to render both loggedin (invisible) and loggedout (visible), 
                        ## and use cookies/jquery to make the menu appear and customize data.  
                        ## i can also use an api query to is_logged_in.
                        ## that technique is used by a lot of large sites like Hulu, as your pages can be 
                        ## cached on a front-end server for quite some time
                        % if request._app_meta.is_logged_in :
                            <ul class="loggedin">
                                <li><a href="/" ${request.nav_section.splash|n}>splash</a></li>
                                <li><a href="/account/home" ${request.nav_section.dashboard|n}>home</a></li>
                                <li><a href="/account/logout">logout</a></li>
                            </ul>
                        % else :
                            <ul class="anonymous">
                                <li><a href="/" ${request.nav_section.splash|n}>splash</a></li>
                                <li><a href="/account/login" ${request.nav_section.login|n}>login</a></li>
                                <li><a href="/account/sign-up" ${request.nav_section.signup|n}>signup</a></li>
                            </ul>
                        % endif
                    </div>
                </div>
            </div>
        </header>
        <div id="content">
            ${self.body()}
        </div>
        <footer>
            <div class="container_12">
                <div class="grid_12">
                    Pyramid ExampleApp
                </div>
            </div>
        </footer>
    </body>
</html>



