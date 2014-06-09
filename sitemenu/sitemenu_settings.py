from django.conf import settings

PAGES = getattr(settings, 'SITEMENU_PAGES', (
    ('text', 'Text page', 'sitemenu.views.render_menupage'),
    ('redr', 'Redirect page', 'sitemenu.views.render_redirectpage'),
    ('indx', 'Index page', 'sitemenu.views.render_menupage'),
))

MENUCLASS = getattr(settings, 'SITEMENU_MENUCLASS', 'sitemenu.models.Menu')


MENU_MAX_LEVELS = getattr(settings, 'SITEMENU_MENU_MAX_LEVELS', 5)
MENU_MAX_ITEMS = getattr(settings, 'SITEMENU_MENU_MAX_ITEMS', 99)

SPLIT_TO_HEADER_AND_FOOTER = getattr(settings, 'SITEMENU_SPLIT_TO_HEADER_AND_FOOTER', False)

PLUGIN_FEEDBACK_FORM = getattr(settings, 'SITEMENU_PLUGIN_FEEDBACK_FORM', 'sitemenu.plugins.feedback_form.forms.FeedbackFormForm')
PLUGIN_FEEDBACK_MODEL = getattr(settings, 'SITEMENU_PLUGIN_FEEDBACK_MODEL', None)
PLUGIN_FEEDBACK_ENABLE_SPAM_FIELD = getattr(settings, 'SITEMENU_PLUGIN_FEEDBACK_ENABLE_SPAM_FIELD', False)

# SERVER CACHE

SERVER_CACHE_DIR = getattr(settings, 'SITEMENU_SERVER_CACHE_DIR', None)
SERVER_CACHE_ARGS_FUNC = getattr(settings, 'SITEMENU_SERVER_CACHE_ARGS_FUNC', None)

# You need to invalidate cache!
# basic method:

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from sitemenu import sitemenu_settings

# from django.contrib.sessions.models import Session
# from qshop.cart.models import Cart, Item, Order
# import shutil

# if sitemenu_settings.SERVER_CACHE_DIR:
#     skip_save_classes = (Session, Cart, Item, Order)

#     @receiver(post_save)
#     def clear_cache_after_save(sender, **kwargs):
#         if not isinstance(kwargs['instance'], skip_save_classes):
#             #print kwargs['instance']
#             shutil.rmtree(sitemenu_settings.SERVER_CACHE_DIR, True)
