from django.urls import include, path, re_path
from django.conf import settings

from .views import dispatcher
from .admin_views import save_menu_position

urlpatterns = [
    path('admin/sitemenu/save_menu_position/', save_menu_position, name='save_menu_position'),
]

if 'sitemenu.plugins.feedback_form' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('feedback-form/', include('sitemenu.plugins.feedback_form.urls')),
    ]


urlpatterns += [
    re_path(r'^(?P<url>.*)$', dispatcher, name='dispatcher'),
]
