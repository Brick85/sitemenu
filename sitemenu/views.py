from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from .sitemenu_settings import MENUCLASS
from . import import_item

Menu = import_item(MENUCLASS)


def dispatcher(request, url):
    url_add = []
    if url == '':
        try:
            menu = Menu.objects.filter(enabled=True, page_type='indx')[0]
        except:
            menu = None
    else:

        if not url.endswith('/'):
            return HttpResponsePermanentRedirect(reverse('dispatcher', kwargs={'url': url + '/'}))
        try:
            menu = Menu.objects.filter(full_url=url, enabled=True)[0]
        except:
            menu = None

        if not menu:
            url_arr = url.split('/')[:-1]
            while url_arr:
                try:
                    menu = Menu.objects.get(enabled=True, full_url='/'.join(url_arr) + '/')
                    break
                except:
                    url_add.append(url_arr[-1])
                    url_arr = url_arr[:-1]

        if menu.page_type == 'indx':
            return HttpResponsePermanentRedirect(reverse('dispatcher', kwargs={'url': ''}))

    if not menu:
        raise Http404

    if menu.redirect_url:
        return HttpResponseRedirect(menu.redirect_url)
    if menu.redirect_to_first_child:
        return HttpResponseRedirect(menu._default_manager.filter(parent=menu)[0].get_absolute_url())

    return menu.render(request, url_add)


def render_menupage(request, menu, url_add):
    if url_add:
        raise Http404
    return render_to_response('sitemenu/simplepage.html', {
            'menu': menu,
            'url_add': url_add,
        }, context_instance=RequestContext(request))


def render_redirectpage(request, menu, url_add):
    if url_add:
        raise Http404
    return HttpResponseRedirect(menu.redirect_url)
