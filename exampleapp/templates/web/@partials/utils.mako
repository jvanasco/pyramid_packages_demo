<%def name="form_textfield_bootstrap_a(form,fieldname,fieldname_display,default_value='',id=None,**webhelpers_kwargs)">
    <%
        css_error= ''
        inline_error= ''
        if form:
            css_error= form.cssError(fieldname)
            if form.hasError(fieldname):
                inline_error= '<span class="help-inline">' + form.getError(fieldname) + '</span>'
        if id:
            id = 'id="%s"' % id
    %>
    <div class="control-group ${css_error}">
        <label for="${fieldname}">${fieldname_display}</label>
        <input type="text" name="${fieldname}" value="${h.text.no_none(default_value)}"/>
        ${inline_error|n}
    </div>
</%def>


<%def name="form_password_bootstrap_a(form,fieldname,fieldname_display,default_value='',id=None,**webhelpers_kwargs)">
    <%
        css_error= ''
        inline_error= ''
        if form:
            css_error= form.cssError(fieldname)
            if form.hasError(fieldname):
                inline_error= '<span class="help-inline">' + form.getError(fieldname) + '</span>'
        if id:
            id = 'id="%s"' % id
    %>
    <div class="control-group ${css_error}">
        <label for="${fieldname}">${fieldname_display}</label>
        <input type="password" name="${fieldname}" value="${h.text.no_none(default_value)}"/>
        ${inline_error|n}
    </div>
</%def>


<%def name="form_checkbox_bootstrap_a(form,fieldname,fieldname_display,default_value='',id=None,**webhelpers_kwargs)">
    <%
        css_error= ''
        inline_error= ''
        if form:
            css_error= form.cssError(fieldname)
            if form.hasError(fieldname):
                inline_error= '<span class="help-inline">' + form.getError(fieldname) + '</span>'
        if id:
            id = 'id="%s"' % id
    %>
    <div class="control-group ${css_error}">
        <label class="control-label" for="${fieldname}">${fieldname_display}</label>
        <input type="checkbox" name="${fieldname}" value="${h.text.no_none(default_value)}" ${id}/>
        ${inline_error|n}
    </div>
</%def>


<%def name="form_submit_bootstrap_a(form,fieldname,fieldname_display,id=None,btn_class='btn-primary')">
    <%
        if id:
            id = 'id="%s"' % id
    %>
    <div class="control-group">
        <input type="submit" class="btn ${btn_class}" name="${fieldname}" value="${fieldname_display}" ${id}/>
    </div>
</%def>


