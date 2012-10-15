from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import importlib
from .sitemenu_settings import PAGES as PAGES_TYPES


class Menu(models.Model):

    PAGES = PAGES_TYPES

    MAX_LEVELS = 5
    MAX_ITEMS = 99
    TYPE_TYPES = [(x[0], x[1]) for x in PAGES]

    # Tree fields
    sort       = models.IntegerField(_('sort'), default=0)
    sortorder  = models.CharField(max_length=MAX_LEVELS * len(str(MAX_ITEMS)), editable=False)
    level      = models.PositiveSmallIntegerField(editable=False, default=0)
    has_childs = models.BooleanField(default=False, editable=False)
    parent     = models.ForeignKey('self', null=True, blank=True)
    parents_list = models.CharField(max_length=MAX_LEVELS * 5, editable=False, null=True, blank=True)

    # Menu field
    full_url       = models.CharField(max_length=255, null=True, blank=True, editable=False, unique=True)
    date_added     = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified  = models.DateTimeField(_('date_modified'), auto_now=True)

    # Misc fields
    page_type               = models.CharField(_('page type'), max_length=4, choices=TYPE_TYPES, default=TYPE_TYPES[0][0])

    title                   = models.CharField(_('title'), max_length=256)
    url                     = models.SlugField(_('url'), max_length=32)

    seo_title               = models.CharField(_('seo title'), max_length=256, null=True, blank=True)
    seo_keywords            = models.CharField(_('seo keywords'), max_length=256, null=True, blank=True)
    seo_description         = models.CharField(_('seo description'), max_length=256, null=True, blank=True)

    content                 = models.TextField(_('content'), blank=True, null=True)

    redirect_url            = models.CharField(_('redirect url'), max_length=256, null=True, blank=True)
    redirect_to_first_child = models.BooleanField(_('redirect ot first child'), default=None)

    enabled                 = models.BooleanField(_('enabled'), default=None)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')
        unique_together = ("url", "parent")
        ordering = ('sortorder',)

    def __unicode__(self):
        return "%s%s" % ("- " * self.level, self.title)

    def save(self, *args, **kwargs):
        if self.get_parent():
            parent = self.get_parent()
            self.parents_list = ';'.join([str(v) for v in parent.get_parents_ids_list() + [parent.pk]])
        else:
            parent = Menu()
            parent.full_url = '/'
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

        super(Menu, self).save(*args, **kwargs)

    def get_parent(self):
        try:
            self._get_parent
        except:
            self._get_parent = self.parent
        return self._get_parent

    def get_parents_ids_list(self):
        return [int(v) for v in filter(None, self.parents_list.split(';'))]

    def get_childs(self):
        return self._default_manager.filter(parent=self).order_by('sort')

    @staticmethod
    def rebuild():
        for menu in Menu.objects.filter(parent=None):
            menu.save()

    def render(self, request, url_add):
        use_page = None
        for page in self.PAGES:
            if page[0] == self.page_type:
                use_page = page
        if not use_page:
            raise KeyError("Could not find page type '%s'" % self.page_type)
        try:
            render_import = use_page[2].split('.')
            render_module = importlib.import_module('.'.join(render_import[:-1]))
            render_function = render_import[-1]
        except ImportError, e:
            raise ImportError("Could not import render function '%s' for menu: %s" % (use_page[2], e))
        try:
            return getattr(render_module, render_function)(request, self, url_add)
        except AttributeError, e:
            raise AttributeError("Could not find render function '%s' in %s" % (render_function, render_module))


