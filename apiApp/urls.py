from django.urls import path
from apiApp import views

urlpatterns = [
    path('course_list/', views.course_list),
    path('course_detail/<int:pk>/', views.course_detail),

    path('student_list/', views.student_list),
    path('student_detail/<int:pk>/', views.student_detail),

    path('food_list/', views.food_list),
    path('food_detail/<int:pk>/', views.food_detail),

]