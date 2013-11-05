from django.conf.urls import patterns, url
from views import save_feedback_form

urlpatterns = patterns('',
    url(r'^send/$', save_feedback_form, name='save_feedback_form'),
)
