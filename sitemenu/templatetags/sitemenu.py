from django import template
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from .. import import_item
from ..sitemenu_settings import MENUCLASS, SPLIT_TO_HEADER_AND_FOOTER
Menu = import_item(MENUCLASS)

register = template.Library()

#from django.core.cache import cache


if SPLIT_TO_HEADER_AND_FOOTER:
    @register.simple_tag(takes_context=True)
    def render_sitemenu_header(context, *args, **kwargs):
        kwargs['nodes'] = Menu.objects.filter(in_top_menu=True)
        return render_sitemenu(context, *args, **kwargs)

    @register.simple_tag(takes_context=True)
    def render_sitemenu_footer(context, *args, **kwargs):
        kwargs['nodes'] = Menu.objects.filter(in_bottom_menu=True)
        return render_sitemenu(context, *args, **kwargs)


@register.simple_tag(takes_context=True)
def set_root_menu(context, var="root_menu"):
    try:
        menu_id = context['menu'].get_parents_ids_list()[0]
        root_menu = Menu.objects.get(pk=menu_id)
    except IndexError:
        root_menu = context['menu']
    context[var] = root_menu
    return ''


@register.simple_tag(takes_context=True)
def render_sitemenu(context, template='_menu', catalogue_root=None, flat=None, exclude_index=None, nodes=None, levels=None):
    if not nodes:
        if not catalogue_root:
            nodes = Menu.objects.filter(enabled=True)
            if flat is not None:
                nodes = nodes.filter(level=0)
        else:
            nodes = Menu.objects.filter(enabled=True, full_url__startswith=catalogue_root.full_url).exclude(pk=catalogue_root.pk)
            if hasattr(catalogue_root, 'q_filters') and catalogue_root.q_filters:
                nodes = nodes.filter(catalogue_root.q_filters)
            if flat is not None:
                nodes = nodes.filter(level=catalogue_root.level + 1)
    if levels is not None:
        try:
            root_level = catalogue_root.level
        except AttributeError:
            root_level = 0
        nodes = nodes.filter(level__lt=root_level + levels)
    if exclude_index is not None:
        nodes = nodes.exclude(page_type='indx')
    return render_to_string('sitemenu/%s.html' % template, {'nodes': nodes}, context_instance=context)


@register.simple_tag(takes_context=True)
def is_activemenu(context, menu, active_text=' class="active"'):
    if menu.is_active(context['request'].get_full_path()):
        return active_text
    else:
        return ''


@register.simple_tag(takes_context=True)
def render_breadcrumbs(context, template='_breadcrumbs', add=None):
    try:
        menu = context['menu']
    except KeyError:
        return ''
    breadcrumbs = menu.get_breadcrumbs()
    return render_to_string('sitemenu/%s.html' % template, {'breadcrumbs': breadcrumbs, 'add': add}, context_instance=context)


@register.simple_tag(takes_context=True)
def render_seometa(context, custom_menu=False):
    if not custom_menu:
        try:
            menu = context['menu']
        except KeyError:
            return ''
    else:
        menu = custom_menu
    return render_to_string('sitemenu/_seometa.html', {'menu': menu}, context_instance=context)


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
            try:
                roots = queryset[0].create_tree(queryset)
            except IndexError:
                return ''
            bits = [self._render_node(context, node) for node in roots]
            return ''.join(bits)

    return RecurseSiteMenuNode(template_nodes, queryset_var)
