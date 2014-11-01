# -*- coding: utf-8 -*-
from django.contrib import admin
from models import FeedbackForm
#from django.utils.translation import ugettext_lazy as _



class FeedbackFormAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'date_added')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.user is not None:
                return ['user'] + obj.FIELDS_FOR_AUTHENICATED_USER + ['date_added', 'ip_address']
            else:
                return obj.FIELDS_FOR_NON_AUTHENICATED_USER + ['date_added', 'ip_address']
        else:
            return self.readonly_fields


    def get_fieldsets(self, request, obj=None):
        form = self.get_form(request, obj, fields=None)
        fields = [field for field in list(form.base_fields) + list(self.get_readonly_fields(request, obj)) if field in self.get_readonly_fields(request, obj)]
        return [(None, {'fields': fields})]


admin.site.register(FeedbackForm, FeedbackFormAdmin)
