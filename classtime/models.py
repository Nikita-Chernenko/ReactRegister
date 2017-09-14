from django.db import models


class ClassTime(models.Model):
    lesson_start = models.TimeField(unique=True)
    lesson_end = models.TimeField(unique=True)

    # def __str__(self):
    #     return "Начало занятия: " + self.lesson_start.strftime("%H/%M")  + " Конец занятия:" + self.lesson_end.strftime("%H/%M")

    def __str__(self):
        return self.lesson_start.strftime("%H/%M") + " - " + self.lesson_end.strftime("%H/%M")
