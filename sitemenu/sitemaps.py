from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from sitemenu.sitemenu_settings import MENUCLASS
from sitemenu import import_item

Menu = import_item(MENUCLASS)


class SiteMenuSitemap(Sitemap):
    def items(self):
        return Menu.objects.filter(enabled=True)

    def lastmod(self, obj):
        if obj.page_type == 'indx':
            return None
        return obj.date_modified

    def location(self, obj):
        if obj.page_type == 'redr':
            return reverse('dispatcher', kwargs={'url': obj.full_url})
        return obj.get_absolute_url()
