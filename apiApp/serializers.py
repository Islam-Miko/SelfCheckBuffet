from rest_framework import serializers
from rest_framework import validators
from .models import *
from .validator_func  import *


class CoursesSerializer(serializers.ModelSerializer):
    """Для создания курса,
    редактирования"""
    name = serializers.CharField(max_length=255, min_length=1,
                                 validators=[
                                     validators.UniqueValidator(queryset=Course.objects.all())
                                 ])
    class Meta:
        model = Course
        fields = '__all__'


class CoursesSerializer2(serializers.ModelSerializer):
    """Для добавления к студенту курса
    Если надо будет работать с нестед json у студента"""
    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    """Получение списка и создание"""
    class Meta:
        model = Food
        fields = '__all__'


class FoodUpdateSerializer(serializers.ModelSerializer):
    """Для редактирования еды"""
    image = serializers.URLField(required=False)
    class Meta:
        model = Food
        fields = '__all__'


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


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    pin = serializers.CharField(max_length=8,
                                min_length=6,
                                required=False)
    class Meta:
        model = UserAdmin
        fields = '__all__'


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
    course = serializers.SlugRelatedField(slug_field='id',
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
    course = serializers.SlugRelatedField(slug_field='id',
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


class Pinserializer(serializers.ModelSerializer):
    """Для вывода долга определенному Пину"""
    class Meta:
        model = Pin
        fields  = ['pin', 'debt']

class PreOperationDetailSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    id = serializers.IntegerField()


class TakingPreOperationSerializer(serializers.Serializer):

    money = serializers.FloatField()
    pin = serializers.CharField(max_length=8,
                                min_length=6)
    products = PreOperationDetailSerializer(many=True)

    def create(self, validated_data):
        pin_info = Pin.objects.filter(pin=validated_data.pop('pin')).get()
        paid_money = validated_data.pop('money')
        products = validated_data.pop('products')


        total_sum_buyed_products = 0
        # total_sum_buyed_products = sum([Food.objects.get(id=product['id']).price for product in products])
        for product in products:
            food = Food.objects.get(id=product['id'])
            price_for_amount_product = food.price * product['amount']
            total_sum_buyed_products += price_for_amount_product

        difference_money_operation = total_sum_buyed_products - paid_money

        debt_sum = 0
        change_money = 0
        OPER_STATUS = 'ACTIVE'
        if difference_money_operation > 0:
            debt_sum = difference_money_operation
        elif difference_money_operation < 0:
            change_money = difference_money_operation
            OPER_STATUS = 'NOTACTIVE'

        pin_info.debt += debt_sum
        pin_info.save()

        operation = Operation.objects.create(pin=pin_info,
                                             total_sum=total_sum_buyed_products,
                                             debt_sum=debt_sum,
                                             status=OPER_STATUS)
        for product in products:
            food_to_oper_detail = Food.objects.get(id=product['id'])
            oper_detail = OperDetail.objects.create(operation=operation,
                                                    food=food_to_oper_detail,
                                                    amount=product['amount'])
            oper_detail.save()
        return operation




{
  "addDate": "2021-07-17T15:18:29.259Z",
  "change": 0,
  "debt": 0,
  "editDate": "2021-07-17T15:18:29.259Z",
  "id": 0,
  "pin": {
    "debt": 0,
    "pin": "string"
  },
  "status": "CLOSED",
  "total": 0
}
class MainOperationCreateSerializer(serializers.Serializer):
    operation = OperationSerializer()
