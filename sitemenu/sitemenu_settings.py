from django.conf import settings

PAGES = getattr(settings, 'SITEMENU_PAGES', (
    ('text', 'Text page', 'sitemenu.views.render_menupage'),
    ('redr', 'Redirect page', 'sitemenu.views.render_redirectpage'),
    ('indx', 'Index page', 'sitemenu.views.render_menupage'),
))

MENUCLASS = getattr(settings, 'SITEMENU_MENUCLASS', 'sitemenu.models.Menu')

SERVER_CACHE_DIR = getattr(settings, 'SITEMENU_SERVER_CACHE_DIR', None)
SERVER_CACHE_ARGS_FUNC = getattr(settings, 'SITEMENU_SERVER_CACHE_ARGS_FUNC', None)
