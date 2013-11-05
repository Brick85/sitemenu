from django import template
from ..forms import FeedbackFormForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
register = template.Library()



@register.simple_tag(takes_context=True)
def render_feedback_form(context):

    request = context['request']
    user = request.user


    form = FeedbackFormForm(request)

    return "<div class='j_feedback_form_container'>" + render_to_string('sitemenu/plugins/feedback_form/feedback_form.html', {'form': form}, context_instance=context) + "</div>"
