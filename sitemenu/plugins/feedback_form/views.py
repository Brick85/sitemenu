#from forms import FeedbackFormForm
from sitemenu.sitemenu_settings import PLUGIN_FEEDBACK_FORM
from sitemenu import import_item
FeedbackFormForm = import_item(PLUGIN_FEEDBACK_FORM)

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _


def save_feedback_form(request):
    if request.method == "POST" and "feedbackformsubmit" in request.POST:
        form = FeedbackFormForm(data=request.POST, request=request)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return render_to_response('sitemenu/plugins/feedback_form/feedback_form_sent.html', {}, context_instance=RequestContext(request))
            else:
                messages.add_message(request, messages.INFO, _('Feedback form sent.'))
                return HttpResponseRedirect('/')
    else:
        form = FeedbackFormForm(request=request)

    return render_to_response('sitemenu/plugins/feedback_form/feedback_form.html', {
            'form': form
        }, context_instance=RequestContext(request))
