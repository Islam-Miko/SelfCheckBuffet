from django.urls import path
from apiApp import views

urlpatterns = [
    path('course_list/', views.course_list),
]