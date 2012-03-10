<%inherit file="/web/@site-template.mako" />
<div class="container_12">
    <div class="grid_12" class="clearfix">
        <h2>
            Account Home! (logged in user's dashboard)
        </h2>
        % if 'facebook_profile' in request.session :
        	Here's the info from facebook
        	<hr/>
        		${request.session['facebook_profile']}
        	<hr/>
        % endif
    </div>
</div>