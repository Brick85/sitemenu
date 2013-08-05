from django.contrib.sitemaps import Sitemap
from sitemenu.sitemenu_settings import MENUCLASS
from sitemenu import import_item

Menu = import_item(MENUCLASS)


class SiteMenuSitemap(Sitemap):
    def items(self):
        return Menu.objects.filter(enabled=True)

    def lastmod(self, obj):
        if obj.page_type == 'indx':
            return ''
        return obj.date_modified

    def location(self, obj):
        return obj.get_absolute_url()
