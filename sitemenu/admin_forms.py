from django import forms
from .models import SiteMenu
from django.utils.translation import ugettext_lazy as _
from .sitemenu_settings import PAGES_DICT


class SiteMenuForm(forms.ModelForm):
    model = SiteMenu

    def clean_page_type(self):
        page_type = self.cleaned_data['page_type'].encode('utf8')

        if PAGES_DICT[page_type]['unique']:
            if self.instance.__class__.objects.filter(page_type=page_type).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('You can create only one page with this type'))
        return self.cleaned_data['page_type']
