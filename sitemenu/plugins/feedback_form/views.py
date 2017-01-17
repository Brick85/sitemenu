from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from sitemenu.sitemenu_settings import PLUGIN_FEEDBACK_FORM
from sitemenu import import_item

FeedbackFormForm = import_item(PLUGIN_FEEDBACK_FORM)


def save_feedback_form(request):
    if request.method == "POST" and "feedbackformsubmit" in request.POST:
        form = FeedbackFormForm(data=request.POST, request=request)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return render(request, 'sitemenu/plugins/feedback_form/feedback_form_sent.html')
            else:
                messages.add_message(request, messages.INFO, _('Feedback form sent.'))
                return HttpResponseRedirect('/')
    else:
        form = FeedbackFormForm(request=request)

    return render(
        request,
        'sitemenu/plugins/feedback_form/feedback_form.html', {
            'form': form
        }
    )
