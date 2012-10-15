from django.conf import settings


FOO_CHOICES = getattr(settings, 'MYAPP_FOO_CHOICES', [('quux', u'Quux')])

PAGES = getattr(settings, 'SITEMENU_PAGES', (
    ('text', 'Text page', 'sitemenu.views.render_menupage'),
    ('redr', 'Redirect page', 'sitemenu.views.render_redirectpage'),
))
