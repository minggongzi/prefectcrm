from django.conf.urls import url,include
from django.contrib import admin
from student import views

urlpatterns = [
    url(r'^/', views.test),
]