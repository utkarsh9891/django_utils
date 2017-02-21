from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class IsNullBlankFilter(SimpleListFilter):
    title = 'Target Field'
    parameter_name = 'target_field'
    show_blank_filter = False
    show_null_filter = True

    def lookups(self, request, model_admin):
        filters = [('0', _('Has value'),)]
        if self.show_null_filter:
            filters.append(('1', _('None'),))
        if self.show_blank_filter:
            filters.append(('2', _('Blank'),))
        if self.show_blank_filter and self.show_null_filter:
            filters.append(('3', _('None or Blank'),))

        return filters

    def queryset(self, request, queryset):
        is_null_kwarg = {
            self.parameter_name: None
        }
        is_blank_kwarg = {
            self.parameter_name: ''
        }
        if self.value() == '0':
            if self.show_null_filter:
                queryset = queryset.exclude(**is_null_kwarg)
            if self.show_blank_filter:
                queryset = queryset.exclude(**is_blank_kwarg)
        elif self.value() == '1':
            queryset = queryset.filter(**is_null_kwarg)
        elif self.value() == '2' and self.show_blank_filter:
            queryset = queryset.filter(**is_blank_kwarg)
        elif self.value() == '3' and self.show_blank_filter:
            queryset = queryset.filter(Q(**is_null_kwarg) | Q(**is_blank_kwarg))

        return queryset
