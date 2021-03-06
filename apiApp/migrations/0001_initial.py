# Generated by Django 3.2.5 on 2021-07-09 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('mentor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ментор')),
                ('assistant', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ассистент')),
                ('class_room', models.CharField(max_length=25, verbose_name='Аудитория')),
                ('start_date', models.DateField(verbose_name='Дата начала курса')),
                ('end_date', models.DateField(verbose_name='Дата окончания курса')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('time', models.CharField(default='08:00', max_length=5, verbose_name='Время')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=0, verbose_name='Количество')),
                ('name', models.CharField(max_length=50, verbose_name='Food')),
                ('image', models.ImageField(upload_to='buffet/', verbose_name='Ссылка на картинку')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('active', models.BooleanField(verbose_name='Наличие на сегодня')),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата операции')),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('total_sum', models.FloatField(verbose_name='Общая сумма к оплате')),
                ('debt_sum', models.FloatField(verbose_name='Сумма долга')),
                ('status', models.CharField(choices=[('ACTIVE', 'Незакрыт'), ('NOTACTIVE', 'Закрыт'), ('NAN', 'Списан')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('active', models.BooleanField(default=True)),
                ('debt', models.FloatField(default=0.0, verbose_name='Долг')),
                ('pin', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='Pin')),
            ],
        ),
        migrations.CreateModel(
            name='UserAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Имя')),
                ('phone', models.CharField(max_length=10, verbose_name='Телефон')),
                ('pin', models.CharField(max_length=8, verbose_name='Пин')),
                ('active', models.BooleanField(default=True, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=25, verbose_name='Имя')),
                ('last_name', models.CharField(default='', max_length=50, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=10, verbose_name='Телефон')),
                ('pin', models.CharField(max_length=8, verbose_name='Пин')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiApp.course', verbose_name='Курс')),
            ],
        ),
        migrations.CreateModel(
            name='OperDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('amount', models.PositiveSmallIntegerField(verbose_name='Количество')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiApp.food')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiApp.operation')),
            ],
        ),
        migrations.AddField(
            model_name='operation',
            name='pin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiApp.pin', verbose_name='Пин студента/юзера'),
        ),
    ]
