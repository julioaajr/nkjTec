from functools import partial
from django.urls import path
from .views import *


urlpatterns =[
    #Views gerais
    path('myschedule/', MySchedule, name ='myschedule'),
    path('fullschedule/', FullSchedule, name ='fullschedule'),
    path('fullschedule/<str:master>/', FullScheduleMaster, name ='fullschedule-master'),
    #cadastrar
    path('reg/procedure/', ProcedureCreate.as_view(), name ='create-procedure'),
    path('reg/status/', StatusCreate.as_view(), name ='create-status'),
    path('reg/payment/', PaymentCreate.as_view(), name ='create-payment'),
    path('reg/appointment/', AppointmentCreate.as_view(), name ='create-appointment'),
    path('reg/schedule/', ScheduleCreate.as_view(), name ='create-schedule'),
    path('reg/dayoff/', DayOffCreate.as_view(), name ='create-dayoff'),
    path('reg/user/', UserCreate.as_view(), name ='create-user'),

    #editar
    path('edit/procedure/<int:pk>/', ProcedureUpdate.as_view(), name ='edit-procedure'),
    path('edit/status/<int:pk>/', StatusUpdate.as_view(), name ='edit-status'),
    path('edit/payment/<int:pk>/', PaymentUpdate.as_view(), name ='edit-payment'),
    path('edit/appointment/<int:pk>/', AppointmentUpdate.as_view(), name ='edit-appointment'),
    path('edit/schedule/<int:pk>/', ScheduleUpdate.as_view(), name ='edit-schedule'),
    path('edit/dayoff/<int:pk>/', DayOffUpdate.as_view(), name ='edit-dayoff'),
    path('edit/user/<int:pk>/', UserUpdate.as_view(), name ='edit-user'),

    #deletar
    path('delete/procedure/<int:pk>/', ProcedureDelete.as_view(), name ='delete-procedure'),
    path('delete/status/<int:pk>/', StatusDelete.as_view(), name ='delete-status'),
    path('delete/payment/<int:pk>/', PaymentDelete.as_view(), name ='delete-payment'),
    path('delete/appointment/<int:pk>/', AppointmentDelete.as_view(), name ='delete-appointment'),
    path('delete/schedule/<int:pk>/', ScheduleDelete.as_view(), name ='delete-schedule'),
    path('delete/dayoff/<int:pk>/', DayOffDelete.as_view(), name ='delete-dayoff'),
    path('delete/user/<int:pk>/', UserDelete.as_view(), name ='delete-user'),

    #listar
    path('list/procedure/', ProcedureList.as_view(), name ='list-procedure'),
    path('list/status/', StatusList.as_view(), name ='list-status'),
    path('list/payment/', PaymentList.as_view(), name ='list-payment'),
    path('list/appointment/', AppointmentList.as_view(), name ='list-appointment'),
    path('list/schedule/', ScheduleList.as_view(), name ='list-schedule'),
    path('list/dayoff/', DayOffList.as_view(), name ='list-dayoff'),
    path('list/users/', UserList.as_view(), name ='list-user'),

]