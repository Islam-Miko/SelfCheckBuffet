from rest_framework import serializers
from .models import *
from .validator_func  import *


class CoursesSerializer(serializers.ModelSerializer):
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


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'

    def validate_pin(self, data):
        if not data.isnumeric():
            raise serializers.ValidationError(['Может содержать лишь цифры!'])

        if len(data) < 6:
            raise serializers.ValidationError(['Длина пина не может быть меньше 6'])



class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdmin
        fields = '__all__'
