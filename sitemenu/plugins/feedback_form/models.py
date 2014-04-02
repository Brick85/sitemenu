from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from sitemenu import import_item
from sitemenu.sitemenu_settings import PLUGIN_FEEDBACK_MODEL


class FeedbackFormAbstract(models.Model):
    message  = models.TextField(_("message"))
    date_added = models.DateTimeField(_("date"), auto_now_add=True)
    ip_address = models.IPAddressField(_("IP"))

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.get_message()

    def get_message(self):
        return self.message.replace('\n', '')
    get_message.allow_tags = True
    get_message.short_description = _('message')

class FeedbackFormBase(FeedbackFormAbstract):
    FIELDS_FOR_AUTHENICATED_USER = ['message']
    FIELDS_FOR_NON_AUTHENICATED_USER = ['user_name', 'user_email', 'user_phone', 'message']
    REQUIRED_FIELDS = ['user_name', ('user_email', 'user_phone'), 'message']
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), blank=True, null=True)
    user_name = models.CharField(_('first name'), max_length=64, blank=True, null=True)
    user_email = models.EmailField(_('email'), blank=True, null=True)
    user_phone = models.CharField(_('phone'), max_length=64, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _('feedback form')
        verbose_name_plural = _('feedback forms')

    def __unicode__(self):
        if self.user:
            return self.user.get_name()
        else:
            return "%s (%s)" % (self.user_name, self.user_email)

class FeedbackForm(import_item(PLUGIN_FEEDBACK_MODEL) if PLUGIN_FEEDBACK_MODEL else FeedbackFormBase):
    pass
