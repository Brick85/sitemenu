from django.conf.urls import patterns, url
from .views import dispatcher
from .admin_views import save_menu_position

urlpatterns = patterns('',
    url(r'^admin/sitemenu/save_menu_position/$', save_menu_position, name='save_menu_position'),
    url(r'^(?P<url>.*)$', dispatcher, name='dispatcher'),
)
