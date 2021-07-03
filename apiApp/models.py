from django.db import models


class Course(models.Model):
    name = models.CharField('Наименование', max_length=255)
    mentor = models.CharField('Ментор', blank=True, max_length=255, null=True)
    assistant = models.CharField('Ассистент', blank=True, max_length=255, null=True)
    class_room = models.CharField('Аудитория', max_length=25)
    start_date = models.DateField(verbose_name='Дата начала курса')
    end_date = models.DateField(verbose_name='Дата окончания курса')
    price = models.FloatField(verbose_name='Azamat')

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField('Имя', max_length=25)
    phone = models.CharField('Телефон', max_length=10)
    pin = models.CharField('Пин', max_length=8)
    course = models.ForeignKey(verbose_name='Курс', to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name




