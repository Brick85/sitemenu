from django.db import models
from django import forms
from django.utils.html import mark_safe
import json

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^sitemenu\.fields\.TableField"])


class TableClass(object):

    def __init__(self, value):
        try:
            self.data = json.loads(value)
        except ValueError:
            self.data = {
                'width': 0,
                'height': 0,
                'table_type': 0,
                'rows': []
            }

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.as_html()

    def as_string(self):
        return json.dumps(self.data)

    def as_html(self):
        html = '<table>'
        if self.data['table_type'] == 1:
            row = self.data['rows'][0]
            html += '<thead>'
            html += '<tr>'
            for j, cell in enumerate(row['data']):
                html += '<th>'
                html += cell
                html += '</th>'
            html += '</tr>'
            html += '</thead>'
        html += '<tbody>'
        for i, row in enumerate(self.data['rows']):
            if i == 0 and self.data['table_type'] == 1:
                continue
            if row['highlight']:
                html += '<tr class="highlight">'
            else:
                html += '<tr>'
            for j, cell in enumerate(row['data']):
                cell_tag = 'td'
                if j == 0 and self.data['table_type'] == 2:
                    cell_tag = 'th'
                html += '<{0}>'.format(cell_tag)
                html += cell
                html += '</{0}>'.format(cell_tag)
            html += '</tr>'
        html += '</tbody>'
        html += '</table>'
        return mark_safe(html)

    def clean_data(self):
        width = self.data['width']
        height = self.data['height']
        self.data['rows'] = [row for i, row in enumerate(self.data['rows']) if i < height]

        for i, row in enumerate(self.data['rows']):
            row['data'] = [cell for j, cell in enumerate(row['data']) if j < width]


class TableField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        kwargs['widget'] = TableWidget(attrs={'class': 'j_tablefield'})
        return super(TableField, self).formfield(**kwargs)

    def to_python(self, value):
        if isinstance(value, TableClass):
            return value
        return TableClass(value)

    def get_prep_value(self, value):
        value.clean_data()
        return value.as_string()


class TableWidget(forms.Textarea):

    class Media:
        css = {
            'all': ('admin/sitemenu/css/tablefield.css',)
        }
        js = ('admin/sitemenu/js/tablefield.js',)

    def render(self, name, value, attrs=None):
        if isinstance(value, TableClass):
            value = value.as_string()
        return super(TableWidget, self).render(name, value, attrs)
