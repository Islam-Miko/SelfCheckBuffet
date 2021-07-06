from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *
from .aux_func import create_pin, get_userAdmin, check_in_DB
from .exceptions import PhonePass, NoInDb


@api_view(['GET', 'POST'])
def course_list(request):
    if request.method == 'GET':
        all_courses = Course.objects.all()
        serializer = CoursesSerializer(all_courses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CoursesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = {
                "message": "Successfully created",
                "item": serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, pk):
    try:
        course = Course.objects.get(id=pk)
    except Course.DoesNotExist:
        return Response('DOESNOTEXIST', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CoursesSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CoursesSerializer(course, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        course.delete()
        return Response('DELETED', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
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
            res = {
                "message": "Successfully created",
                "item": serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response('Student does not exist', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response('DELETED', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def food_list(request):
    if request.method == 'GET':
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = {
                "message": "Successfully created",
                "item": serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def food_detail(request, pk):
    try:
        food = Food.objects.get(id=pk)
    except Food.DoesNotExist:
        return Response('Food does not exist', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        user = UserAdmin.objects.all()
        serializer = UserAdminSerializer(user, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            data_with_pin = create_pin(request.data)
        except PhonePass:
            return Response('Поле телефон обязательное!')
        serializer = UserAdminSerializer(data=data_with_pin)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = {
                "message" : "Successfully created",
                "item" : serializer.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user_ = UserAdmin.objects.get(id=pk)
    except UserAdmin.DoesNotExist:
        return Response('Does not exist', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserAdminSerializer(user_)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserAdminSerializer(user_, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_.delete()
        return Response('DELETED', status=status.HTTP_204_NO_CONTENT)





@api_view(['POST'])
def authentication(request):
    serializer = AuthenticationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_name = get_userAdmin(serializer.data)
    if user_name is None:
        res = {
            "message": False
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    if user_name.pin == serializer.data['userPin']:
        res = {
            "message": True
        }
        return Response(res, status=status.HTTP_200_OK)
    else:
        res = {
            "message": False
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search(request, name):
    students = Student.objects.filter(name=name)
    if students:
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    return Response(False, status=status.HTTP_404_NOT_FOUND)

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