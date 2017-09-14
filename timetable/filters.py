import django_filters
from timetable.models import ClassTime, ScheduledSubject


# class ClassTimeFilter(django_filters.FilterSet):
#     lesson_start__gte = django_filters.TimeFilter(name="lesson_start", lookup_expr='gte')
#     lesson_end__lte = django_filters.TimeFilter(name="lesson_end", lookup_expr='lte')
#
#     class Meta:
#         model = ClassTime
#         fields = ['lesson_start', 'lesson_end']

class ScheduledSubjectFilter(django_filters.FilterSet):
    lesson_start__gte = django_filters.TimeFilter(name="class_time__lesson_start", lookup_expr='gte')
    lesson_end__lte = django_filters.TimeFilter(name="class_time__lesson_end", lookup_expr='lte')
    date__gte = django_filters.DateFilter(name="date", lookup_expr='gte')
    date__lte = django_filters.DateFilter(name="date", lookup_expr='lte')

    class Meta:
        model = ScheduledSubject
        fields = ['lesson_start__gte','lesson_end__lte','date__gte','date__lte']