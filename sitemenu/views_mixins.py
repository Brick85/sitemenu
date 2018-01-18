from django.http import Http404

class ContextMixin(object):
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_context_dict())
        return super(ContextMixin, self).get_context_data(**kwargs)

    def get_context_dict(self):
        return {}

class SitemenuViewMixin(object):
    def dispatch(self, request, menu, url_add):
        self.process_url_add(request, menu, url_add)
        return super(SitemenuViewMixin, self).dispatch(request, menu, url_add)

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_context_dict())
        kwargs['menu'] = self.kwargs['menu']
        return super(SitemenuViewMixin, self).get_context_data(**kwargs)

    def process_url_add(self, request, menu, url_add):
        if len(url_add) > 0:
            raise Http404

    def get_context_dict(self):
        return {}
