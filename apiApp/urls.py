from django.urls import path
from apiApp import views

urlpatterns = [
    path('course', views.course_list),
    path('course/<int:pk>', views.course_detail),

    path('student', views.student_list),
    path('student/<int:pk>', views.student_detail),

    path('food_list/', views.food_list),
    path('food_detail/<int:pk>/', views.food_detail),

    path('user', views.user_list),
    path('user<int:pk>/', views.user_detail),

    path('user/auth', views.authentication),

    path('search_student/<str:name>/', views.search),

    path('courses/', views.active_courses),

    # url for flutter

    path('food/', views.FoodActiveList.as_view()),


    # path('imageLoad/', views.ImageLoad.as_view()),

    # path('pin_list/', views.pin_list),
    # path('pin_detail/<int:pk>/', views.pin_detail),

]