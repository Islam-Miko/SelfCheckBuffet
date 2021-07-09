from rest_framework import serializers
from rest_framework import validators
from .models import *
from .validator_func  import *


class CoursesSerializer(serializers.ModelSerializer):
    """Для создания курса"""
    name = serializers.CharField(max_length=255, min_length=1,
                                 validators=[
                                     validators.UniqueValidator(queryset=Course.objects.all())
                                 ])
    class Meta:
        model = Course
        fields = '__all__'

class CoursesSerializer2(serializers.ModelSerializer):
    """Для добавления к студенту курса"""
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'




class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


# class PinSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pin
#         fields = '__all__'
#
#     def validate_pin(self, data):
#         if not data.isnumeric():
#             raise serializers.ValidationError(['Может содержать лишь цифры!'])
#
#         if len(data) < 6:
#             raise serializers.ValidationError(['Длина пина не может быть меньше 6'])


class UserAdminSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(min_length=1,
                                 max_length=25)
    phone = serializers.CharField(max_length=10,
                                  min_length=10,
                                  validators=[
                                      check_for_numberic,
                                  ])
    pin = serializers.CharField(max_length=8,
                                min_length=6,
                                validators=[
                                    validators.UniqueValidator(queryset=Pin.objects.all())
                                ])
    active = serializers.BooleanField(default=True,
                                      required=False)

    def create(self, validated_data):
        pin_ob = validated_data.get('pin')
        new_pin = Pin.objects.create(pin=pin_ob)
        new_pin.save()
        return UserAdmin.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.active = validated_data.get('active', instance.active)
        instance.pin = validated_data.get('pin', instance.pin)
        instance.save()
        return instance


class StudentSerializer2(serializers.Serializer):
    """Создание нового студента"""
    id = serializers.ReadOnlyField()
    active = serializers.BooleanField()
    name = serializers.CharField(max_length=25,
                                 min_length=1)
    last_name = serializers.CharField(max_length=50,
                                      min_length=1)
    phone = serializers.CharField(max_length=10,
                                  min_length=10,
                                  validators=[
                                      check_for_numberic,
                                  ])
    pin = serializers.CharField(max_length=8,
                                min_length=6,
                                validators=[validators.UniqueValidator(queryset=Pin.objects.all())])
    course = serializers.SlugRelatedField(slug_field='name',
                                          queryset=Course.objects.all()
                                          )

    def create(self, validated_data):
        pin_ob = validated_data.get('pin')
        new_pin = Pin.objects.create(pin=pin_ob)
        new_pin.save()
        return Student.objects.create(**validated_data)

        # pin_ob = validated_data.get('pin')
        # course = validated_data.pop('course')
        # new_or_old, flag = Course.objects.get_or_create(**course)
        # if flag:
        #     new_or_old.save()
        # new_pin = Pin.objects.create(pin=pin_ob)
        # new_pin.save()
        # return Student.objects.create(course=new_or_old, **validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.course = validated_data.get('course', instance.course)
        instance.pin = validated_data.get('pin', instance.pin)
        instance.save()
        return instance

class StudentUpdateSerializer(serializers.ModelSerializer):
    """Сериалайзер для редактирования студента"""
    pin = serializers.CharField(max_length=8,
                                min_length=6)
    course = serializers.SlugRelatedField(slug_field='name',
                                          queryset=Course.objects.all()
                                          )
    class Meta:
        model = Student
        fields = '__all__'

class AuthenticationSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=10,
                                      max_length=10,
                                      validators=[
                                          check_for_numberic,
                                      ])
    pin = serializers.CharField(max_length=8,
                                    min_length=6,
                                    validators=[
                                        check_for_numberic,
                                    ])




class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'