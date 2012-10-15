from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Menu


def dispatcher(request, url):
    if not url.endswith('/'):
        return HttpResponseRedirect(reverse('dispatcher', kwargs={'url': url + '/'}))
    try:
        menu = Menu.objects.filter(full_url='/' + url, enabled=True)[0]
    except:
        menu = None

    url_add = []
    if not menu:
        url_arr = url.split('/')[:-1]
        while url_arr:
            try:
                menu = Menu.objects.get(enabled=True, full_url='/' + '/'.join(url_arr) + '/')
                break
            except:
                url_add.append(url_arr[-1])
                url_arr = url_arr[:-1]

    if not menu:
        raise Http404

    return menu.render(request, url_add)


def render_menupage(request, menu, url_add):
    if url_add:
        raise Http404
    return render_to_response('sitemenu/default.html', {
            'menu': menu,
            'url_add': url_add,
        }, context_instance=RequestContext(request))


def render_redirectpage(request, menu, url_add):
    if url_add:
        raise Http404
    return HttpResponseRedirect(menu.redirect_url)
