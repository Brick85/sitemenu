from django import forms
from models import FeedbackForm
from django.utils.translation import ugettext_lazy as _
from sitemenu.helpers import get_client_ip
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from sitemenu.sitemenu_settings import PLUGIN_FEEDBACK_ENABLE_SPAM_FIELD


class FeedbackFormForm(forms.ModelForm):
    error_messages = {
        'required_field': _('This field is required.'),
        'at_least_one_required': _('At least one field must be filled.'),
    }
    if PLUGIN_FEEDBACK_ENABLE_SPAM_FIELD:
        surname = forms.CharField(required=False)

    class Meta:
        model = FeedbackForm

    def __init__(self, request, *args, **kwargs):
        f = super(FeedbackFormForm, self).__init__(*args, **kwargs)
        self.request = request

        if PLUGIN_FEEDBACK_ENABLE_SPAM_FIELD:
            self.fields['surname'].widget.attrs['class'] = 'spm_cls'

        self.__delete_fields__()

        self.custom_init(request)

        return f

    def __delete_fields__(self):
        if self.request.user.is_authenticated():
            fields_to_use = FeedbackForm.FIELDS_FOR_AUTHENICATED_USER
        else:
            fields_to_use = FeedbackForm.FIELDS_FOR_NON_AUTHENICATED_USER

        if PLUGIN_FEEDBACK_ENABLE_SPAM_FIELD:
            fields = fields_to_use + ['surname']
        else:
            fields = fields_to_use

        fields_to_del = []
        for field in self.fields:
            if field not in fields:
                fields_to_del.append(field)

        for field in fields_to_del:
            del self.fields[field]

        self.fields.keyOrder = fields

    def custom_init(self, request):
        pass

    def clean(self):
        cd = self.cleaned_data


        if PLUGIN_FEEDBACK_ENABLE_SPAM_FIELD:
            if 'surname' in cd and cd['surname']:
                raise forms.ValidationError("Spam message!")

        for field in FeedbackForm.REQUIRED_FIELDS:
            if type(field) == tuple:
                if all([gfield in cd for gfield in field]):
                    if not any([(cd[gfield]) for gfield in field]):
                        for gfield in field:
                            self._errors[gfield] = self.error_class([FeedbackFormForm.error_messages['at_least_one_required']])
                            if gfield in cd:
                                del cd[gfield]
            else:
                if field not in self.fields:
                    continue
                if not field in cd or not cd[field]:
                    self._errors[field] = self.error_class([FeedbackFormForm.error_messages['required_field']])
                    if field in cd:
                        del cd[field]

        return cd

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(FeedbackFormForm, self).save(*args, **kwargs)
        obj.ip_address = get_client_ip(self.request)
        if self.request.user.is_authenticated():
            obj.user = self.request.user
        obj.save()


        body = render_to_string("sitemenu/plugins/feedback_form/mail_body.html", {'obj': obj})
        subject = render_to_string("sitemenu/plugins/feedback_form/mail_subject.txt", {'obj': obj}).strip()
        email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [mail for name, mail in settings.MANAGERS])
        email.content_subtype = "html"
        email.send()
