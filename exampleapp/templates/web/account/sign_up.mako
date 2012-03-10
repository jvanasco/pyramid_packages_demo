<%inherit file="/web/@site-template.mako" />

<div class="container_12">
	<div class="grid_6">
		<h3>Sign up using Facebook</h3>
			<a href="${fb.oauth_code__url_dialog()}">
				Connect with <strong>Facebook</strong>
			</a>
			<script>
				$(document).ready( function() {
					signup_page_redirect();
					fbUtils.ensureInit(fbUtils.signup_page_facebook_init);
				});
			</script>
			<p>
				Or
			</p>
			<a href="#" id="signup-start_btn-email">
				Create an account using my e-mail address
				<form action="/account/sign-up" method="POST">
					<input type="text" name="email_address" value="email address" />
					<input type="text" name="username" value="username" />
					<input type="submit" name="submit" value="submit"/>
				</form>
			</a>
	</div>
</div>
