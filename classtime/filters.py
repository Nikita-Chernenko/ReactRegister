import django_filters
from classtime.models import ClassTime


class ClassTimeFilter(django_filters.FilterSet):
    lesson_start__qte = django_filters.TimeFilter(name="lesson_start", lookup_expr="gte")
    lesson_end__lte = django_filters.TimeFilter(name="lesson_end", lookup_expr="lte")

    class Meta:
        model = ClassTime
        fields = ["lesson_start__qte", "lesson_end__lte"]
