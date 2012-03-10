<%inherit file="/web/@site-template.mako" />
<div class="container_12">
	<div class="grid_8">
		<div class="tout-shaded" id="login-splash">
			<h2>Welcome back, Friend.</h2>
				<h4>Log In with Facebook</h4>
				<script>
					$(document).ready( function() {
					    console.log('login.html - $(document).ready()');
					    utils.getLoginStatus();
						fbUtils.ensureInit(fbUtils.login_page_facebook_init);
					});
				</script>
				
				A few things you should know about this page.
				
				<ul>
					<li>two ways to implement a facebook login button are shown below.</li>
					<li>
						<p>
							Notice the onload function that we have running here.  also look at <a href="/js/web.js">the web.js file</a>. 
						</p>
						<p>
							I found the facebook developer API docs to have been seriously lacking a while back ( they may be better now ), and devised a 'best practices' technique that I really like.  I documented it here: <a href="http://www.destructuring.net/2011/12/08/facebook-developer-notes-javascript-sdk-and-asynchronous-woes/">http://www.destructuring.net/2011/12/08/facebook-developer-notes-javascript-sdk-and-asynchronous-woes/</a>
						</p>
						<p>
							When you see the underlying python code in web_account.py, you'll note that I have 2 different endpoints -- as a 'login' and a 'signup' are a bit different.  To handle the automatic login, the fbUtils.login_page_facebook_init sends a few key variables from facebook.  We're then able to validate the encrypted payload and communicate with facebook.
						</p>
						<p>
							Please note that you need to log out of Facebook in order to stop the redirect from happening.  I believe that you must do the facebook logout as part of their API terms of service.
						</p>
<pre>
	$(document).ready( function() {
		console.log('login.html - $(document).ready()');
		utils.getLoginStatus();
		fbUtils.ensureInit(fbUtils.login_page_facebook_init);
	});
</pre>
					</li>
					
				</ul>


				
				<ul>
					<li>
						<span><fb:login-button registration-url="/account/sign-up" scope="${fb.app_scope}"></span>
						<br/>
						&lt;fb:login-button registration-url="/account/sign-up" scope="${fb.app_scope}"/&gt;
					</li>
					<li>
						<div class="fb-login-button">Login with Facebook</div>
						&lt;div class="fb-login-button"&gt;Login with Facebook&lt;/div&gt;
					</li>
				</ul>

				<h4>Log In with E-Mail</h4>
				
					<p>
						a valid account is : 'user@domain.com' + 'password'
					</p>
				
					<form:error name="Error_Main"/>
					<form action="/account/login" method="POST">
						<input type="hidden" name="m" value="submit" />
						<div class="textInput" id="inputFirst">
							<input id="login-email_address" name="email_address" placeholder="Email Address" size="30" type="text" />
						</div>
						<div class="textInput" id="">
						  <input id="login-password" name="password" placeholder="Password" size="30" type="password" />
						</div>
						<div class="textInput" id="inputLast">
						  <input id="login-remember_me" name="remember_me" value="1" type="checkbox" />Remember Me
						</div>
						<input type="submit" id="login-btn-login" class="" value="login" name="login"/>
					</form>
		</div>
	</div>
	<div class="grid_8">
		<a href="/account/sign-up">Sign Up Page</a>
	</div>
</div>

