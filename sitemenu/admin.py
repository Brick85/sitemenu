from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .sitemenu_settings import MENUCLASS


class SiteMenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("title",)}
    list_display = ('title', 'enabled')

    class Media:
        css = {
            'screen': ('/static/admin/sitemenu/css/no-theme/jquery-ui-1.9.0.custom.min.css', '/static/admin/sitemenu/css/sitemenu.css',),
        }

    def __init__(self, *args, **kwargs):
        super(SiteMenuAdmin, self).__init__(*args, **kwargs)

        self.list_display = list(self.list_display)

        if 'indented_short_title' not in self.list_display:
            if self.list_display[0] == 'action_checkbox':
                self.list_display[1] = 'indented_short_title'
            else:
                self.list_display[0] = 'indented_short_title'
        self.list_display_links = ('indented_short_title',)

        if 'actions_column' not in self.list_display:
            self.list_display.append('actions_column')

    def indented_short_title(self, item):
        title = item.title
        span = '<span class="result_list__ident_span"></span>' * item.level
        return mark_safe('%s%s' % (span, title))
    indented_short_title.short_description = _('title')
    indented_short_title.allow_tags = True

    def _actions_column(self, instance):
        return ('<div class="drag_handle"></div>',)

    def actions_column(self, instance):
        return u' '.join(self._actions_column(instance))
    actions_column.allow_tags = True
    actions_column.short_description = _('actions')


if MENUCLASS == 'sitemenu.models.Menu':
    from .models import Menu
    admin.site.register(Menu, SiteMenuAdmin)
