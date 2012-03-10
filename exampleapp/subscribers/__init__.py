
## this is from akhet, mike orr's scaffold

from ..lib import helpers

def add_renderer_globals(event):
    """A subscriber for ``pyramid.events.BeforeRender`` events.  I update
    the :term:`renderer globals` with values that are familiar to Pylons
    users.
    """
    renderer_globals = event
    renderer_globals["h"] = helpers
    request = event.get("request") or threadlocal.get_current_request()
    if not request:
        return
    tmpl_context = request.tmpl_context
    renderer_globals["c"] = tmpl_context
    renderer_globals["tmpl_context"] = tmpl_context
    try:
        renderer_globals["session"] = request.session
    except ConfigurationError:
        pass
    #renderer_globals["url"] = request.url_generator
