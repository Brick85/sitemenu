from django import template
from django.template import RequestContext
from django.template.loader import get_template
from django.utils.translation import get_language

from citycars.settings import LANGUAGES
from site_menu.models import Menu


register = template.Library()


def get_menu(context, name, template):
    header_node = Menu.objects.get(enabled=True, url=name)
    nodes = header_node.get_descendants().filter(enabled=1, level__lte=header_node.level + 2)
    c = RequestContext(context['request'], {'nodes': nodes})
    t = get_template('menu/%s.html'%template)
    menu = t.render(c)
    return menu
register.simple_tag(takes_context=True)(get_menu)

def get_languages_menu(context, active_text='active', template='_languages'):
    path = context['request'].get_full_path()
    current_ln = get_language()
    lang = []
    for ln in LANGUAGES:
        active = ''
        if current_ln==ln[0]:
            active = active_text
        lang.append({
            'name': ln[1],
            'code' : ln[0],
            'active': active,
            'link': path.replace('/%s/'%current_ln, '/%s/'%ln[0])
        })
    c = RequestContext(context['request'], {'lang': lang})
    t = get_template('menu/%s.html'%template)
    menu = t.render(c)
    return menu
register.simple_tag(takes_context=True)(get_languages_menu)


def is_active(context, menu, active_text='active'):
    if menu.is_active(context['request'].get_full_path()):
        return active_text
    else:
        return ''
register.simple_tag(takes_context=True)(is_active)

