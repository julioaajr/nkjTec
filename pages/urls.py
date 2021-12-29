from functools import partial
from django.urls import path
from .views import *


urlpatterns =[
    #cadastrar
    path('', Index, name ='index'),
]