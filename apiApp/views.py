import datetime

from django.db.models import Sum
from rest_framework import views
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .aux_func import create_pin, get_userAdmin
from .exceptions import PhonePass


@api_view(['GET', 'POST'])
@csrf_exempt
def course_list(request):
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
    if request.method == 'GET':
        students = Student.objects.all().order_by('id')
        serializer = StudentSerializer2(students, many=True)
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
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer2(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StudentSerializer2(student, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@csrf_exempt
def food_list(request):
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
    try:
        food = Food.objects.get(id=pk)
    except Food.DoesNotExist:
        return Response(False, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FoodSerializer(food, data=request.data)
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
        serializer = UserAdminSerializer(user_, data=request.data)
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
def search(request, name):
    students = Student.objects.filter(name__icontains=f'{name}').all().order_by('last_name')
    if students:
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    return Response(False, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def active_courses(request):
    all_active_courses = Course.objects.filter(start_date__lte=datetime.datetime.now(),
                                               end_date__gt=datetime.datetime.now()).order_by('id')
    serializer = CoursesSerializer(all_active_courses, many=True)
    return Response(serializer.data)


class FoodActiveList(views.APIView):
    def get(self, request):
        all_active_food = Food.objects.filter(active=True).order_by('id')
        serializer = FoodSerializer(all_active_food, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@csrf_exempt
def pin_debt(request, pin):
    debt_in_operation = Operation.objects.filter(pin=pin).values('pin').annotate(total_debt=Sum('debt_sum'))
    return Response(debt_in_operation)


class OperationView(views.APIView):
    def get(self, request):
        operations = Operation.objects.all()
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationPinView(views.APIView):
    def get(self, request, pin):
        operations = Operation.objects.filter(pin=pin)
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)


class OperationDebtPinView(views.APIView):
    def get(self, request, pin):
        operations = Operation.objects.filter(pin=pin, status='ACTIVE')
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)






# @api_view(['GET', 'POST'])
# def pin_list(request):
#     if request.method == 'GET':
#         foods = Pin.objects.all()
#         serializer = PinSerializer(foods, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = PinSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response('Successfully created', status=status.HTTP_201_CREATED)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def pin_detail(request, pk):
#     try:
#         pin = Pin.objects.get(id=pk)
#     except Pin.DoesNotExist:
#         return Response('Pin does not exist', status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PinSerializer(pin)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = PinSerializer(pin, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         pin.delete()
#         return Response('DELETED', status=status.HTTP_204_NO_CONTENT)