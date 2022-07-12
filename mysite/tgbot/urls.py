from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('oldman/ex1', views.telegram_webhook)
]
