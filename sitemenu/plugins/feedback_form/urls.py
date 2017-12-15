from django.conf.urls import url
from .views import save_feedback_form

urlpatterns = [
    url(r'^send/$', save_feedback_form, name='save_feedback_form'),
]
