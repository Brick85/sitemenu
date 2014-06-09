from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from .sitemenu_settings import PAGES as PAGES_TYPES, MENUCLASS, SPLIT_TO_HEADER_AND_FOOTER, MENU_MAX_LEVELS, MENU_MAX_ITEMS
from . import import_item


class SiteMenu(models.Model):
    _translation_fields = ['title', 'h1_title', 'page_title', 'seo_keywords', 'seo_description', 'content']

    PAGES = PAGES_TYPES

    TYPE_TYPES = [(x[0], x[1]) for x in PAGES]

    # Tree fields
    sort       = models.IntegerField(_('sort'), default=0, editable=False)
    sortorder  = models.CharField(max_length=MENU_MAX_LEVELS * len(str(MENU_MAX_ITEMS)), editable=False)
    level      = models.PositiveSmallIntegerField(editable=False, default=0)
    has_childs = models.BooleanField(default=False, editable=False)
    parent     = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent'))
    parents_list = models.CharField(max_length=MENU_MAX_LEVELS * 5, editable=False, null=True, blank=True)

    # Menu field
    full_url       = models.CharField(max_length=255, null=True, blank=True, editable=False, unique=True)
    date_added     = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified  = models.DateTimeField(_('date modified'), auto_now=True)

    # Misc fields
    page_type               = models.CharField(_('page type'), max_length=4, choices=TYPE_TYPES, default=TYPE_TYPES[0][0])

    title                   = models.CharField(_('title'), max_length=256)
    url                     = models.SlugField(_('url'), max_length=32)

    h1_title                = models.CharField(_('h1 title'), max_length=256, blank=True)
    page_title              = models.CharField(_('page title'), max_length=256, blank=True)
    seo_keywords            = models.CharField(_('seo keywords'), max_length=256, blank=True)
    seo_description         = models.CharField(_('seo description'), max_length=256, blank=True)

    content                 = models.TextField(_('content'), blank=True)

    redirect_url            = models.CharField(_('redirect url'), max_length=256, blank=True)
    redirect_to_first_child = models.BooleanField(_('redirect to first child'), default=None)

    enabled                 = models.BooleanField(_('enabled'), default=None)

    if SPLIT_TO_HEADER_AND_FOOTER:
        in_top_menu = models.BooleanField(_('show in top menu'), default=False)
        in_bottom_menu = models.BooleanField(_('show in bottom menu'), default=False)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')
        unique_together = ("url", "parent")
        ordering = ('sortorder',)
        abstract = True

    def __unicode__(self):
        return "%s%s" % ("- " * self.level, self.title)

    def save(self, skip_tree_update=False, rebuild_sort=False, *args, **kwargs):
        if not skip_tree_update:
            if self.get_parent():
                parent = self.get_parent()
                self.parents_list = ';'.join([str(v) for v in parent.get_parents_ids_list() + [parent.pk]])
                # if not parent.has_childs:
                #     parent.has_childs = True
                #     parent.save(skip_tree_update=True)
            else:
                class Parent:
                    pass
                parent = Parent()
                parent.full_url = ''
                parent.level = -1
                parent.sortorder = ''
                parent.parents_list = ''
                self.parents_list = ''

            self.full_url = "%s%s/" % (parent.full_url, self.url)
            self.level = parent.level + 1

            if not self.pk:
                try:
                    siblings = parent.get_childs(only_enabled=False)
                except AttributeError:
                    siblings = self._default_manager.filter(parent=None)
                try:
                    self.sort = siblings.aggregate(models.Max('sort'))['sort__max'] + 1
                except TypeError:
                    self.sort = 0

            self.sortorder = parent.sortorder + ('%' + '0%dd' % len(str(MENU_MAX_ITEMS))) % self.sort

            self.has_childs = False
            tmp_sort = 1
            for child in self.get_childs(only_enabled=False):
                self.has_childs = True
                child._get_parent = self
                if rebuild_sort:
                    child.sort = tmp_sort
                    tmp_sort += 1
                child.save(rebuild_sort=rebuild_sort)

            if not self.has_childs:
                self.redirect_to_first_child = False

        super(SiteMenu, self).save(*args, **kwargs)

    def get_parent(self):
        try:
            self._get_parent
        except:
            self._get_parent = self.parent
        return self._get_parent

    def get_parents_ids_list(self):
        return [int(v) for v in filter(None, self.parents_list.split(';'))]

    def get_childs(self, only_enabled=True):
        cache_key = '_get_childs'
        if only_enabled:
            cache_key += '_enabled'
        if not hasattr(self, cache_key):
            childs = self._default_manager.filter(parent=self).order_by('sort')
            if only_enabled:
                childs = childs.filter(enabled=True)
            setattr(self, cache_key, childs)
        return getattr(self, cache_key)

    def create_tree(self, queryset):
        current_path = []
        top_nodes = []
        root_level = None
        for obj in queryset:
            node_level = obj.level
            if root_level is None:
                root_level = node_level
            if node_level < root_level:
                raise ValueError(_("cache_tree_children was passed nodes in the wrong order!"))
            obj._get_childs_enabled = []

            while len(current_path) > node_level - root_level:
                current_path.pop(-1)
            if node_level == root_level:
                top_nodes.append(obj)
            else:
                current_path[-1]._get_childs_enabled.append(obj)
            current_path.append(obj)
        return top_nodes

    def rebuild(self, rebuild_sort=False):
        tmp_sort = 1
        for menu in self._default_manager.filter(parent=None):
            if rebuild_sort:
                menu.sort = tmp_sort
                tmp_sort += 1
            menu.save(rebuild_sort=rebuild_sort)

    if SPLIT_TO_HEADER_AND_FOOTER:
        def rebuild_intop_and_inbottom_menu(self):
            for menu in self._default_manager.filter(parent=None):
                menu.apply_attr_to_all_childs('in_top_menu')
                menu.apply_attr_to_all_childs('in_bottom_menu')

    def apply_attr_to_all_childs(self, attr):
        attr_value = getattr(self, attr)
        for child in self.get_childs(only_enabled=False):
            setattr(child, attr, attr_value)
            child.save(skip_tree_update=True)
            child.apply_attr_to_all_childs(attr)

    def render(self, request, url_add):
        use_page = None
        for page in self.PAGES:
            if page[0] == self.page_type:
                use_page = page
        if not use_page:
            aviable_pages = []
            for page in self.PAGES:
                aviable_pages.append(page[0])
            raise KeyError("Could not find page type '%s' in '%s'" % (self.page_type, ', '.join(aviable_pages)))

        return import_item(use_page[2])(request, self, url_add)

    def get_absolute_url(self):
        if self.redirect_url:
            if self.redirect_url.startswith('/'):
                return reverse('dispatcher', args=(self.redirect_url[1:],))
            else:
                return self.redirect_url
        if self.redirect_to_first_child:
            return self._default_manager.filter(parent=self)[0].get_absolute_url()
        if self.page_type == 'indx':
            return reverse('dispatcher', kwargs={'url': ''})
        return reverse('dispatcher', kwargs={'url': self.full_url})

    def is_active(self, full_path):
        if full_path == '/' and self.page_type == 'indx':
            return True
        return '/' + self.full_url in full_path

    def get_breadcrumbs(self):
        return self._default_manager.filter(pk__in=self.get_parents_ids_list() + [self.pk])

    def get_page_title(self):
        if self.page_type == 'indx':
            return None
        if hasattr(self, '_page_title'):
            return self._page_title
        if hasattr(self, 'page_title') and self.page_title:
            return self.page_title
        return self.title

    def get_h1_title(self):
        if hasattr(self, '_h1_title'):
            return self._h1_title
        if hasattr(self, 'h1_title') and self.h1_title:
            return self.h1_title
        return self.title

if MENUCLASS == 'sitemenu.models.Menu':
    class Menu(SiteMenu):
        pass
