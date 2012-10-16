from django import template
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from .. import import_item
from ..sitemenu_settings import MENUCLASS
Menu = import_item(MENUCLASS)

register = template.Library()


def render_sitemenu(context, name=None, template='_menu'):
    nodes = Menu.objects.filter(enabled=True)
    return render_to_string('sitemenu/%s.html' % template, {'nodes': nodes}, context_instance=context)
register.simple_tag(takes_context=True)(render_sitemenu)


def is_activemenu(context, menu, active_text=' class="active"'):
    if menu.is_active(context['request'].get_full_path()):
        return active_text
    else:
        return ''
register.simple_tag(takes_context=True)(is_activemenu)


def render_breadcrumbs(context, template='_breadcrumbs'):
    try:
        menu = context['menu']
    except KeyError:
        return ''
    breadcrumbs = menu.get_breadcrumbs()
    return render_to_string('sitemenu/%s.html' % template, {'breadcrumbs': breadcrumbs}, context_instance=context)
register.simple_tag(takes_context=True)(render_breadcrumbs)


@register.tag
def recurse_sitemenu(parser, token):
    """
    Based on MPTT recursetree tag

    Iterates over the nodes in the tree, and renders the contained block for each node.
    This tag will recursively render children into the template variable {{ children }}.
    Only one database query is required (children are cached for the whole tree)

    Usage:
        <ul>
            {% recurse_sitemenu nodes %}
                <li>
                    {{ node.title }}
                    {% if node.has_childs %}
                        <ul>
                            {{ children }}
                        </ul>
                    {% endif %}
                </li>
            {% endrecurse_sitemenu %}
        </ul>
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(_('%s tag requires a queryset') % bits[0])

    queryset_var = bits[1]

    template_nodes = parser.parse(('endrecurse_sitemenu',))
    parser.delete_first_token()

    class RecurseSiteMenuNode(template.Node):
        def __init__(self, template_nodes, queryset_var):
            self.template_nodes = template_nodes
            self.queryset_var = queryset_var

        def _render_node(self, context, node):
            bits = []
            context.push()
            for child in node.get_childs():
                context['node'] = child
                bits.append(self._render_node(context, child))
            context['node'] = node
            context['children'] = mark_safe(u''.join(bits))
            rendered = self.template_nodes.render(context)
            context.pop()
            return rendered

        def render(self, context):
            queryset = context[self.queryset_var]
            roots = queryset[0].create_tree(queryset)
            bits = [self._render_node(context, node) for node in roots]
            return ''.join(bits)

    return RecurseSiteMenuNode(template_nodes, queryset_var)
