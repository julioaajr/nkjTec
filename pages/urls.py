from functools import partial
from django.urls import path
from .views import *


urlpatterns =[
    #cadastrar
    path('', IndexView.as_view(), name ='index'),
]