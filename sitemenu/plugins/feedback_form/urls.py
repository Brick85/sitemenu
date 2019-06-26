from django.conf.urls import path
from .views import save_feedback_form

urlpatterns = [
    path('send/', save_feedback_form, name='save_feedback_form'),
]
