from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SiteMenu
from .sitemenu_settings import PAGES


class SiteMenuForm(forms.ModelForm):
    model = SiteMenu

    def clean_page_type(self):
        page_type = self.cleaned_data.get('page_type')

        if self.is_page_type_have_to_be_uniq(page_type):
            if self.instance.__class__.objects.filter(page_type=page_type).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('You can create only one page with this type'))
        return page_type

    def is_page_type_have_to_be_uniq(self, page_type):
        """
        Find out page_type and check unique attribute
        """
        for p in PAGES:
            try:
                if p[0] == page_type and p[3]:
                    return True
            except IndexError:
                pass
        else:
            return False
