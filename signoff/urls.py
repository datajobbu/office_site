from django.contrib import admin
from django.urls import path

from .views import index, signoff, detail, request_create


app_name = 'signoff'

urlpatterns = [
    path('', index, name='list'),
    path('signoff/', signoff, name="signoff"),
    path('signoff/<str:date>/', detail),
    path('create/', request_create, name="request_create"),
]
