from django import template
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.template import RequestContext
from django.template.loader import get_template
import re
from .. import import_item
from ..sitemenu_settings import MENUCLASS, SPLIT_TO_HEADER_AND_FOOTER, LANGUAGES, DIGG_PAGINATOR_SHOW_PAGES
Menu = import_item(MENUCLASS)

register = template.Library()
from django.urls import translate_url


if SPLIT_TO_HEADER_AND_FOOTER:
    @register.simple_tag(takes_context=True)
    def render_sitemenu_header(context, *args, **kwargs):
        kwargs['nodes'] = Menu.objects.filter(enabled=True, in_top_menu=True)
        return render_sitemenu(context, *args, **kwargs)

    @register.simple_tag(takes_context=True)
    def render_sitemenu_footer(context, *args, **kwargs):
        kwargs['nodes'] = Menu.objects.filter(enabled=True, in_bottom_menu=True)
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

@register.tag(name="digg_pagination")
def do_digg_pagination(parser, token):
    try:
        tag_name, current_page, total_pages = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    nodelist = parser.parse(('end_digg_pagination',))
    parser.delete_first_token()
    return DiggPaginationNode(nodelist, current_page, total_pages)

class DiggPaginationNode(template.Node):
    def __init__(self, nodelist, current_page, total_pages):
        self.nodelist = nodelist
        self.current_page = template.Variable(current_page)
        self.total_pages = template.Variable(total_pages)

    def render(self, context):
        current_page = self.current_page.resolve(context)
        total_pages = self.total_pages.resolve(context)

        if total_pages <= 0:
            return ''

        output = ''

        if total_pages <= DIGG_PAGINATOR_SHOW_PAGES + 4:
            pages = range(1, total_pages+1)
        else:
            pages = [1]
            if current_page < DIGG_PAGINATOR_SHOW_PAGES:
                pages += range(2,DIGG_PAGINATOR_SHOW_PAGES + 3)
                pages += [0]
            elif current_page > total_pages - DIGG_PAGINATOR_SHOW_PAGES + 1:
                pages += [0]
                pages += range(total_pages - DIGG_PAGINATOR_SHOW_PAGES - 1, total_pages)
            else:
                pages += [0]
                pages += range(current_page - DIGG_PAGINATOR_SHOW_PAGES/2, current_page + DIGG_PAGINATOR_SHOW_PAGES/2 + 1)
                pages += [0]
            pages += [total_pages]

        # print "%02d" % current_page, ["%02d" % i for i in pages]

        for i in pages:
            context['iterpage'] = {
                'num': i,
                'active': True if i == current_page else False,
                'is_spacer': True if i == 0 else False
            }
            output += self.nodelist.render(context)
        return output


@register.tag(name="highlight_results")
def do_highlight_results(parser, token):
    try:
        tag_name, highlite_text = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one argument" % token.contents.split()[0])
    nodelist = parser.parse(('end_highlight_results',))
    parser.delete_first_token()
    return HighlightResultsNode(nodelist, highlite_text)

class HighlightResultsNode(template.Node):
    def __init__(self, nodelist, highlite_text):
        self.nodelist = nodelist
        self.highlite_text = template.Variable(highlite_text)

    def render(self, context):
        highlite_text = self.highlite_text.resolve(context)
        output = self.nodelist.render(context)

        if highlite_text is None or len(highlite_text) == 0:
            return output

        pattern = re.compile(highlite_text, re.IGNORECASE)
        output_hl = ""
        i = 0
        for m in pattern.finditer(output):
            output_hl += "".join([output[i:m.start()],
                       "<span class='hl'>",
                       output[m.start():m.end()],
                       "</span>"])
            i = m.end()
        output_hl += output[i:]

        return output_hl


@register.simple_tag(takes_context=True)
def render_sitemenu(context, template='_menu', catalogue_root=None, flat=None, exclude_index=None, nodes=None, levels=None):
    if nodes is None:
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
    return render_to_string('sitemenu/%s.html' % template, {'nodes': nodes}, request=context['request'])


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
    return render_to_string('sitemenu/%s.html' % template, {'breadcrumbs': breadcrumbs, 'add': add}, request=context['request'])


@register.simple_tag(takes_context=True)
def render_seometa(context, custom_menu=False):
    if not custom_menu:
        try:
            menu = context['menu']
        except KeyError:
            return ''
    else:
        menu = custom_menu
    return render_to_string('sitemenu/_seometa.html', {'menu': menu}, request=context['request'])


@register.simple_tag(takes_context=True)
def get_languages_menu(context):
    path = context['request'].get_full_path()
    current_ln = get_language()
    langs = []

    for ln in LANGUAGES:
        langs.append({
            'name': ln[1],
            'code': ln[0],
            'link': translate_url(path, ln[0]),
            'active': True if current_ln == ln[0] else False
        })

    return render_to_string('sitemenu/_languages.html', {'langs': langs,})



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
                roots = queryset.model.create_tree(queryset)
            except IndexError:
                return ''
            bits = [self._render_node(context, node) for node in roots]
            return ''.join(bits)

    return RecurseSiteMenuNode(template_nodes, queryset_var)
