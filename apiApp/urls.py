from django.urls import path
from apiApp import views

urlpatterns = [
    path('course', views.course_list),
    # Получение списка всех курсов, создание нового курса(GET, POST)
    path('course/<int:pk>', views.course_detail),
    # Получение одного курса по id, изменение его данных (GET, PUT)

    path('student', views.student_list),
    # Получение списка всех студентов, создание нового студента(GET, POST)
    path('student/<int:pk>', views.student_detail),
    # Получение одного студента по id, изменение его данных (GET, PUT)

    path('food/', views.food_list),
    # Получение списка всех выпечек, создание новой выпечки(GET, POST)
    path('food/<int:pk>/', views.food_detail),
    # Получение одной выпечки по id, изменение его данных (GET, PUT)
    path('food/<int:status>', views.FoodActiveList.as_view()),
    # Получение списка по статусу 1 - True, 0 - False

    path('user', views.user_list),
    # Получение списка всех юзеров, создание нового юзера (GET, POST)
    path('user/<int:pk>', views.user_detail),
    # Получение одного юзера по id, изменение его данных (GET, PUT)
    path('user/auth', views.authentication),
    # Аутентификация юзера
# """
#     path('search_student/<str:name>/', views.search),
#
#     path('courses/', views.active_courses),
#
#
# 
#     path('pin/<str:pin>', views.pin_debt),
#
#
#     path('operation', views.OperationView.as_view()),
#     # Для создания операции (POST)
#     path('operation/<str:pin>', views.OperationPinView.as_view()),
#     # Показывает оперцаю совершенную юзерам с pin
#     path('operation/debt/<str:pin>', views.OperationDebtPinView.as_view()),
#     # path('pin/make/payment', views.payment),
#
# """

    # path('imageLoad/', views.ImageLoad.as_view()),

    # path('pin_list/', views.pin_list),
    # path('pin_detail/<int:pk>/', views.pin_detail),

]