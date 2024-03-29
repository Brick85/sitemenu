from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .sitemenu_settings import MENUCLASS
from django.conf import settings
from .admin_forms import SiteMenuForm
from .admin_views import save_menu_position
from django.urls import path



if 'modeltranslation' in settings.INSTALLED_APPS:
    from modeltranslation.admin import TranslationAdmin
    ParentModel = TranslationAdmin
else:
    ParentModel = admin.ModelAdmin

if 'ckeditor_uploader' in settings.INSTALLED_APPS:
    from django.db import models
    from ckeditor_uploader.widgets import CKEditorUploadingWidget
    sitemenu_formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }
elif 'ckeditor' in settings.INSTALLED_APPS:
    from django.db import models
    from ckeditor.widgets import CKEditorWidget
    sitemenu_formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }
else:
    sitemenu_formfield_overrides = {}


class SiteMenuAdmin(ParentModel):
    prepopulated_fields = {"url": ("title",)}
    list_display = ('title', 'enabled')
    formfield_overrides = sitemenu_formfield_overrides
    change_list_template = 'admin/sitemenu/sitemenu_change_list.html'
    form = SiteMenuForm

    class Media:
        css = {
            'screen': (
                'admin/sitemenu/css/no-theme/jquery-ui.min.css',
                'admin/sitemenu/css/sitemenu.css',
                'admin/sitemenu/css/images.css',
            ),
        }

        # ordering is important !!! and first file (sitemenu.js) ends })})(jQuery);
        # all other files ends with })(django.jQuery);
        js = (
            'admin/sitemenu/js/sitemenu.js',
            'admin/sitemenu/js/images.js',
            'admin/sitemenu/js/jquery-ui.min.js',
        )

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
        title = "<span class='menu_level_%s'>%s</span>" % (item.level, item.title)
        span = '<span class="result_list__ident_span"></span>' * item.level
        return mark_safe('%s%s<div class="drag_handle_container"><div class="drag_handle"></div></div>' % (span, title))
    indented_short_title.short_description = _('title')
    indented_short_title.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reorder-menu-position/', self.admin_site.admin_view(save_menu_position), name='reorder-menu-position')
        ]

        return custom_urls + urls


if MENUCLASS == 'sitemenu.models.Menu':
    from .models import Menu
    admin.site.register(Menu, SiteMenuAdmin)
