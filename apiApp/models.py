from django.db import models


class Course(models.Model):
    name = models.CharField('Наименование', max_length=255)
    mentor = models.CharField('Ментор', blank=True, max_length=255, null=True)
    assistant = models.CharField('Ассистент', blank=True, max_length=255, null=True)
    class_room = models.CharField('Аудитория', max_length=25)
    start_date = models.DateField(verbose_name='Дата начала курса')
    end_date = models.DateField(verbose_name='Дата окончания курса')
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField('Имя', max_length=25)
    phone = models.CharField('Телефон', max_length=10)
    pin = models.CharField('Пин', max_length=8)
    course = models.ForeignKey(verbose_name='Курс', to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserAdmin(models.Model):
    name = models.CharField('Имя', max_length=25)
    phone = models.CharField('Телефон', max_length=10)
    pin = models.CharField('Пин', max_length=8)
    active = models.BooleanField(verbose_name='Status', default=True)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField('Food', max_length=50)
    image = models.URLField(verbose_name='Ссылка на картинку')
    price = models.FloatField('Цена')
    active = models.BooleanField(verbose_name='Наличие на сегодня')

    def __str__(self):
        return self.name


class Pin(models.Model):
    pin = models.CharField('Pin', max_length=8,
                           primary_key=True)

    def __str__(self):
        return f'Пин: {self.pin}'

STATUS_CHOICES = (
    ('ACTIVE', 'Незакрыт'),
    ('NOTACTIVE', 'Закрыт'),
    ('NAN', 'Списан'),
)

class Operation(models.Model):
    add_date = models.DateTimeField(verbose_name='Дата операции',
                                    auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE,
                            verbose_name='Пин студента/юзера')
    total_sum = models.FloatField('Общая сумма к оплате')
    debt_sum = models.FloatField('Сумма долга')
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    def __str__(self):
        return f' Операция совершенная {self.pin}'


class OperDetail(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    def __str__(self):
        return f' Операция {self.food} на {self.operation}'