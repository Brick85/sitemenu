from django.conf.urls import patterns, include, url
from .views import dispatcher

urlpatterns = patterns('',
    url(r'^(?P<url>.*)$', dispatcher, name='dispatcher'),
)
