from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from .sitemenu_settings import PAGES as PAGES_TYPES, MENUCLASS
from . import import_item


class SiteMenu(models.Model):

    PAGES = PAGES_TYPES

    MAX_LEVELS = 5
    MAX_ITEMS = 99
    TYPE_TYPES = [(x[0], x[1]) for x in PAGES]

    # Tree fields
    sort       = models.IntegerField(_('sort'), default=0)
    sortorder  = models.CharField(max_length=MAX_LEVELS * len(str(MAX_ITEMS)), editable=False)
    level      = models.PositiveSmallIntegerField(editable=False, default=0)
    has_childs = models.BooleanField(default=False, editable=False)
    parent     = models.ForeignKey('self', null=True, blank=True, verbose_name=_('parent'))
    parents_list = models.CharField(max_length=MAX_LEVELS * 5, editable=False, null=True, blank=True)

    # Menu field
    full_url       = models.CharField(max_length=255, null=True, blank=True, editable=False, unique=True)
    date_added     = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified  = models.DateTimeField(_('date modified'), auto_now=True)

    # Misc fields
    page_type               = models.CharField(_('page type'), max_length=4, choices=TYPE_TYPES, default=TYPE_TYPES[0][0])

    title                   = models.CharField(_('title'), max_length=256)
    url                     = models.SlugField(_('url'), max_length=32)

    seo_title               = models.CharField(_('seo title'), max_length=256, null=True, blank=True)
    seo_keywords            = models.CharField(_('seo keywords'), max_length=256, null=True, blank=True)
    seo_description         = models.CharField(_('seo description'), max_length=256, null=True, blank=True)

    content                 = models.TextField(_('content'), blank=True, null=True)

    redirect_url            = models.CharField(_('redirect url'), max_length=256, null=True, blank=True)
    redirect_to_first_child = models.BooleanField(_('redirect to first child'), default=None)

    enabled                 = models.BooleanField(_('enabled'), default=None)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')
        unique_together = ("url", "parent")
        ordering = ('sortorder',)
        abstract = True

    def __unicode__(self):
        return "%s%s" % ("- " * self.level, self.title)

    def save(self, skip_tree_update=False, *args, **kwargs):
        if not skip_tree_update:
            if self.get_parent():
                parent = self.get_parent()
                self.parents_list = ';'.join([str(v) for v in parent.get_parents_ids_list() + [parent.pk]])
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

            self.sortorder = parent.sortorder + ('%' + '0%dd' % len(str(self.MAX_ITEMS))) % self.sort

            self.has_childs = False

            for child in self.get_childs():
                self.has_childs = True
                child._get_parent = self
                child.save()

        super(SiteMenu, self).save(*args, **kwargs)

    def get_parent(self):
        try:
            self._get_parent
        except:
            self._get_parent = self.parent
        return self._get_parent

    def get_parents_ids_list(self):
        return [int(v) for v in filter(None, self.parents_list.split(';'))]

    def get_childs(self):
        try:
            self._get_childs
        except:
            self._get_childs = self._default_manager.filter(parent=self).order_by('sort')
        return self._get_childs

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
            obj._get_childs = []

            while len(current_path) > node_level - root_level:
                current_path.pop(-1)
            if node_level == root_level:
                top_nodes.append(obj)
            else:
                current_path[-1]._get_childs.append(obj)
            current_path.append(obj)
        return top_nodes

    def rebuild(self):
        for menu in self._default_manager.filter(parent=None):
            menu.save()

    def render(self, request, url_add):
        use_page = None
        for page in self.PAGES:
            if page[0] == self.page_type:
                use_page = page
        if not use_page:
            raise KeyError("Could not find page type '%s'" % self.page_type)

        return import_item(use_page[2])(request, self, url_add)

    def get_absolute_url(self):
        if self.redirect_url:
            return self.redirect_url
        if self.redirect_to_first_child:
            return self._default_manager.filter(parent=self)[0].get_absolute_url()
        if self.page_type == 'indx':
            return '/'
        return reverse('dispatcher', kwargs={'url': self.full_url})

    def is_active(self, full_path):
        return self.full_url in full_path

    def get_breadcrumbs(self):

        return self._default_manager.filter(pk__in=self.get_parents_ids_list() + [self.pk])

if MENUCLASS == 'sitemenu.models.Menu':
    class Menu(SiteMenu):
        pass
