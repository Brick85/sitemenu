from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.utils.deconstruct import deconstructible


try:
    from pytils.translit import translify
except ImportError:
    translify = lambda x: x
import re
slugify_replace_pattern = re.compile('[^\w\.]+')


def get_paginated_list(objects, page, on_page):
    paginator = Paginator(objects, on_page)

    try:
        objects_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        raise Http404('There is no such page')

    return objects_page


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@deconstructible
class UploadToSlugify(object):
    def slugify_and_transliterate(self, string):
        return slugify_replace_pattern.sub('_', translify(string))

    def __init__(self, basedir):
        self.basedir = basedir

    def __call__(self, instance, filename):
        filename_slug = self.slugify_and_transliterate(filename)
        return u"%s/%s" % (self.basedir, filename_slug)
upload_to_slugify = UploadToSlugify
