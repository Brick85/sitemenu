class ContextMixin(object):
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_context_dict())
        return super(ContextMixin, self).get_context_data(**kwargs)

class SitemenuViewMixin(object):
    def get_context_data(self, **kwargs):
        kwargs.update(self.get_context_dict())
        kwargs['menu'] = self.kwargs['menu']
        return super(SitemenuViewMixin, self).get_context_data(**kwargs)

