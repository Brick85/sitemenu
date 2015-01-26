from django.conf import settings


class ImagesPopupMixin(object):
    class Media:
        js = (
            settings.STATIC_URL + 'admin/sitemenu/js/images.js',
        )
        css = {
            'screen': (settings.STATIC_URL + 'admin/sitemenu/css/images.css',),
        }
