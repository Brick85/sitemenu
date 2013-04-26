from django.db import models
from django import forms
from django.contrib.admin import widgets as admin_widgets

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^sitemenu\.fields\.TableField"])

class TableField(models.TextField):

    def formfield(self, **kwargs):
        kwargs['widget'] = TableWidget(attrs={'class': 'j_tablefield'})
        return super(TableField, self).formfield(**kwargs)


class TableWidget(forms.Textarea):

    class Media:
        css = {
            'all': ('admin/sitemenu/css/tablefield.css',)
        }
        js = ('admin/sitemenu/js/tablefield.js',)

