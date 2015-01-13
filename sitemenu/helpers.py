from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

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

def slugify_and_transliterate(string):
    return slugify_replace_pattern.sub('_', translify(string))


def upload_to_slugify(basedir):
    def make_upload_path(instance, filename):
        filename_slug = slugify_and_transliterate(filename)
        return u"%s/%s" % (basedir, filename_slug)
    return make_upload_path
