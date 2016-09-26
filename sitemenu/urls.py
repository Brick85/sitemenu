from django.conf.urls import url, include
from django.conf import settings
from .views import dispatcher
from .admin_views import save_menu_position

urlpatterns = [
    url(r'^admin/sitemenu/save_menu_position/$', save_menu_position, name='save_menu_position'),
]

if 'sitemenu.plugins.feedback_form' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^feedback-form/', include('sitemenu.plugins.feedback_form.urls')),
    ]


urlpatterns += [
    url(r'^(?P<url>.*)$', dispatcher, name='dispatcher'),
]
