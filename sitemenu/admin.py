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

    def indented_short_title(self, item):
        title = item.title
        span = '<span class="result_list__ident_span"></span>' * item.level
        return mark_safe('%s%s<div class="drag_handle_container"><div class="drag_handle"></div></div>' % (span, title))
    indented_short_title.short_description = _('title')
    indented_short_title.allow_tags = True


if MENUCLASS == 'sitemenu.models.Menu':
    from .models import Menu
    admin.site.register(Menu, SiteMenuAdmin)
