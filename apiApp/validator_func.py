from rest_framework import serializers
from .models import UserAdmin


def check_for_numberic(phone):
    if not phone.isdigit():
        raise serializers.ValidationError(['Может содержать только цифры!'])


def check_in_db(phone):
    user_admin = UserAdmin.objects.filter(phone=phone).last()
    if not user_admin:
        raise serializers.ValidationError(['Нету в системе!'])

