var console = window['console'];

var utils= {
	_login_check : false,
	_is_logged_in : false,
	is_logged_in : function(){ return this._is_logged_in ; },
	errorHandler : function(){},
	getLoginStatus : function() {
		$.ajax({ 
			url:'/api/internal/is-logged-in',
			success:function(data,textStatus, jqXHR){
			    utils._login_check = true;
			    if ( data['logged-in'] ) { 
					console.log("utils:getLoginStatus - user is logged in.");
			    	utils._is_logged_in = true ; 
			    } 
			    else {
					console.log("utils:getLoginStatus - user is not logged in.");
			    }
			},
			error:function (jqXHR, textStatus, errorThrown){
				console.log("utils:getLoginStatus - error");
			}        	
		});
	}
}


function is_logged_in(){
	console.log('is_logged_in - always return false');
	return false;
}

function signup_page_redirect() {
	console.log('signup_page_redirect');
	if ( is_logged_in() ) {
		window.location('/account/home');
	}
}



var fbUtils= {
	scope:'email',
	logout: function(){logout();},
	_initialized : false,
	isInitialized: function() { return this._initialized; },
	// wrap all our facebook init stuff within a function that runs post async, but is cached across the site
	initialize : function(){
		this._initialized= true;
		while ( this._runOnInit.length ) { (this._runOnInit.pop())(); }
	},
	ensureInit :  function(callback) {
		if(!fbUtils._initialized) {
			setTimeout(function() {fbUtils.ensureInit(callback);}, 50);
		} else {
			if(callback) { callback(); }
		}
	},	
	_runOnInit: [],
	runOnInit: function(f) {
		if(this._initialized) {
			f();
		} else {
			this._runOnInit.push(f);
		}		
	},
	handle_login_status : function(){
			FB.getLoginStatus(
				function(response){
					console.log('FB.getLoginStatus');
					console.log(response);
					if (response.authResponse) {
						console.log('-authenticated');
						console.log('-authResponse.accessToken ' + response.authResponse.accessToken);
						console.log('-authResponse.accessToken ' + response.authResponse.signedRequest);
						console.log('-authResponse.userID ' + response.authResponse.userID);
					} else {
						console.log('-not authenticated');
					}
				}
			);
		}
	, 
	event_listener_tests : function(){	
		FB.Event.subscribe('auth.login', function(response){
		  console.log('auth.login');
		  console.log(response);
		});
		FB.Event.subscribe('auth.logout', function(response){
			  console.log('auth.logout');
			  console.log(response);
		});
		FB.Event.subscribe('auth.authResponseChange', function(response){
			  console.log('auth.authResponseChange');
			  console.log(response);
		});
		FB.Event.subscribe('auth.statusChange', function(response){
			  console.log('auth.statusChange');
			  console.log(response);
		});
	},
	signup_page_facebook_init : function(){
		console.log('signup_page_facebook_init');
		FB.getLoginStatus(
			function(response){
				console.log('signup_page_facebook_init - FB.getLoginStatus(response)');
				console.log(response);
				if (response.authResponse) {
					// redirect if logged in to facebook-authenticate
					var redirect = "/account/facebook-authenticate?redirectedFrom=signup&accessToken=" + response.authResponse.accessToken + "&signedRequest=" + response.authResponse.signedRequest + "&userID=" + response.authResponse.userID;
					console.log("redirecting to... " + redirect);
					if ( 1 ) { window.location = redirect; }
				}
			}
		);
	},
	login_page_facebook_init : function(){
		console.log('login_page_facebook_init');
		FB.getLoginStatus(
			function(response){
				console.log('login_page_facebook_init - FB.getLoginStatus(response)');
				console.log(response);
				if (response.authResponse) {
					console.log('logged in');
					var redirect = "/account/facebook-authenticate?redirectedFrom=login&accessToken=" + response.authResponse.accessToken + "&signedRequest=" + response.authResponse.signedRequest + "&userID=" + response.authResponse.userID;
					console.log("redirecting to... " + redirect);
					if ( 1 ) { window.location = redirect; }
				}
			}
		);
	}
}


