from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

def get_paginated_list(objects, page, on_page):
    paginator = Paginator(objects, on_page)

    try:
        objects_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        raise Http404('There is no such page')

    return objects_page
