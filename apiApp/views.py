from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


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
            return Response('Succesfully created', status=status.HTTP_201_CREATED)
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
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Succesfully created', status=status.HTTP_201_CREATED)
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
            return Response('Successfully created', status=status.HTTP_201_CREATED)

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        food.delete()
        return Response('DELETED', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def pin_list(request):
    if request.method == 'GET':
        foods = Pin.objects.all()
        serializer = PinSerializer(foods, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PinSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully created', status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def pin_detail(request, pk):
    try:
        pin = Pin.objects.get(id=pk)
    except Pin.DoesNotExist:
        return Response('Pin does not exist', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PinSerializer(pin)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PinSerializer(pin, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pin.delete()
        return Response('DELETED', status=status.HTTP_204_NO_CONTENT)