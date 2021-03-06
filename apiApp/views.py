import datetime

from django.db.models import Sum, Q
from rest_framework import views
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .serializers import *
from .aux_func import *
from .exceptions import PhonePass


@api_view(['GET', 'POST'])
@csrf_exempt
def course_list(request):
    """Создание курса"""
    if request.method == 'GET':
        all_courses = Course.objects.all().order_by('id')
        serializer = CoursesSerializer(all_courses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CoursesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@csrf_exempt
def course_detail(request, pk):
    """редактирование курса"""
    try:
        course = Course.objects.get(id=pk)
    except Course.DoesNotExist:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CoursesSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CoursesSerializer(course, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@csrf_exempt
def student_list(request):
    """Создание студента"""
    if request.method == 'GET':
        students = Student.objects.all().order_by('id')
        serializer = StudentSerializer4(students, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            data_with_pin = create_pin(request.data)
        except PhonePass:
            return Response('Поле телефон обязательное!')
        serializer = StudentSerializer2(data=data_with_pin)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@csrf_exempt
def student_detail(request, pk):
    """Редактирование студента"""
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer4(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StudentUpdateSerializer(student, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@csrf_exempt
def food_list(request):
    """Создание и список выпечек"""
    if request.method == 'GET':
        foods = Food.objects.all().order_by('id')
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@csrf_exempt
def food_detail(request, pk):
    """Редактирование выпечки"""
    try:
        food = Food.objects.get(id=pk)
    except Food.DoesNotExist:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FoodUpdateSerializer(food, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET', 'POST'])
@csrf_exempt
def user_list(request):
    """Получение списка юзеров, создание нового юзера"""
    if request.method == 'GET':
        user = UserAdmin.objects.all().order_by('id')
        serializer = UserAdminSerializer(user, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            data_with_pin = create_pin(request.data)
        except PhonePass:
            return Response('Поле телефон обязательное!', status=status.HTTP_400_BAD_REQUEST)
        serializer = UserAdminSerializer(data=data_with_pin)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@csrf_exempt
def user_detail(request, pk):
    """Получение юзера по id
    редактирование"""
    try:
        user_ = UserAdmin.objects.get(id=pk)
    except UserAdmin.DoesNotExist:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserAdminSerializer(user_)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserAdminUpdateSerializer(user_, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@csrf_exempt
def authentication(request):
    """Аутентификация юзера по номеру и пину"""
    serializer = AuthenticationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user_name = get_userAdmin(serializer.data)
        res = {
                "success": True,
                "message": "Добро Пожаловать"
            }
        return Response(res, status=status.HTTP_200_OK)
    except UserAdmin.DoesNotExist:
        res = {
            "success": False
        }
        return Response(res, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def search(request):
    """Для поиска по ФИо"""
    name = request.query_params.get('name')
    last_name = request.query_params.get('last_name')
    students_by_lastname = Student.objects.filter(last_name__icontains=f'{last_name}'
                                      ).all().order_by('last_name')
    students_by_name = Student.objects.filter(name__icontains=f'{name}'
                                                  ).all().order_by('name')
    students = students_by_lastname.union(students_by_name)
    if students:
        serializer = StudentSerializer4(students, many=True)
        return Response(serializer.data)
    return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def active_courses(request):
    """Для получения активных курсов, при редактировании студентов или создании студентов
    """
    all_active_courses = Course.objects.filter(start_date__lte=datetime.datetime.now(),
                                               end_date__gt=datetime.datetime.now()).order_by('id')
    serializer = CoursesSerializer(all_active_courses, many=True)
    return Response(serializer.data)


class FoodActiveList(views.APIView):
    """Для получения активных на сегодня выпечек,
    мобприложение"""
    def get(self, request, status):
        all_active_food = Food.objects.filter(active=status).order_by('id')
        serializer = FoodSerializer(all_active_food, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@csrf_exempt
def pin_debt(request, pin):
    """Выводит долг для пина"""
    debt_in_operation = Pin.objects.filter(pin=pin).get()
    serializer = Pinserializer(debt_in_operation)
    return Response(serializer.data)


class OperationView(views.APIView):
    # def get(self, request):
    #     operations = Operation.objects.all()
    #     serializer = OperationSerializer(operations, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        try:
            entrance_serializer = TakingPreOperationSerializer(data=request.data)
            entrance_serializer.is_valid(raise_exception=True)
            pin = entrance_serializer.data.pop('pin')
            money = entrance_serializer.data.pop('money')
            products = entrance_serializer.data.pop('products')

            buyer_by_pin = get_buyer_by_pin(pin)

            total_sum_to_pay = get_total_sum_for_products(products)
            debt_sum, change_money, OPER_STATUS = determine_DCOP(total_sum_to_pay, money)
            take_A_note_to_pin_debt(debt_sum, buyer_by_pin)
            data_to_opertaion = {
                "pin" : buyer_by_pin,
                "status": OPER_STATUS,
                "debt_sum": debt_sum,
                "total_sum": total_sum_to_pay,
                "product" : products,
            }
            opera = make_a_operation(data_to_opertaion)
            datas = {
                "id": opera.id,
                "pin": {"pin" : buyer_by_pin.pin,
                        "debt" : buyer_by_pin.debt
                        },
                "add_date" : opera.add_date,
                "edit_date" : opera.edit_date,
                "change" : change_money,
                "status" : OPER_STATUS,
                "debt_sum" : debt_sum,
                "total_sum" : total_sum_to_pay
            }
            main_result_serializer = MainOperationCreateSerializer(datas)
            return Response(main_result_serializer.data)
        except Pin.DoesNotExist:
            return Response({'error':'NO such PIN'}, status=status.HTTP_404_NOT_FOUND)
        except Food.DoesNotExist:
            return Response({'error':'NO Food with such ID'},status=status.HTTP_404_NOT_FOUND)

class OperationPinView(views.APIView):
    def get(self, request, pin):
        pin_obj = Pin.objects.filter(pin=pin).get()
        serializer = PinAllSerializer(pin_obj)
        return Response(serializer.data)


class OperationDebtPinView(views.APIView):
    def get(self, request, pin):
        operations = Operation.objects.filter(pin=pin, status='ACTIVE')
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)


# class OperationDebtPinView(views.APIView):
#     def get(self, request, pin):
#         operations = Operation.objects.filter(pin=pin, status='ACTIVE')
#         serializer = OperationSerializer(operations, many=True)
#         return Response(serializer.data)


class MakePaymentView(views.APIView):
    """Взнос денег для закрытия долгов"""
    def put(self, request):
        serializer = PaymentDataTaking(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pin_instance = Pin.objects.filter(pin=serializer.data.pop('pin')).get()
        except Pin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        payment = request.data['payment']
        change = computate_change(pin_instance, payment)
        change_operation_status(pin_instance, payment-change)
        data = {
                "change": change,
                "payment": payment,
                "debt": pin_instance.debt
            }
        serializer = PaymentSerializer(data)
        return Response(serializer.data)


class OperationDetailPin(views.APIView):
    """View для вывода операций совершенных в долг.
    При закрытии долгов, в мобприложении, будут видны долговые операции"""
    def get(self, request, pin):
        pin_instance = Pin.objects.filter(pin=pin).get()
        active_operations = Operation.objects.filter(pin=pin_instance, status='ACTIVE')
        serializer = OperationDetailPinSerializer(active_operations, many=True)
        return Response(serializer.data)











