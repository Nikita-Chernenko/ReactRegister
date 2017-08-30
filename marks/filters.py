import django_filters

from marks.models import Mark


class MarkValueFilter(django_filters.FilterSet):
    min_value = django_filters.NumberFilter(name="value", lookup_expr='gte')
    max_value = django_filters.NumberFilter(name="value", lookup_expr='lte')

    class Meta:
        model = Mark
        fields = ['min_value', 'max_value']
