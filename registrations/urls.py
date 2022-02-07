from functools import partial
from django.urls import path
from .views import *


urlpatterns =[
    #Views gerais
    path('myschedule/', MySchedule, name ='myschedule'),
    path('allschedules/', AllSchedules, name ='allschedules'),
    path('allschedules/<str:nickmaster>/', AllSchedulesMaster, name ='allschedules-master'),
    path('passrecovery/', PassRecovery, name ='passrecovery'),
    path('passchange/', PassChange, name ='passchange'),
    #cadastrar
    path('reg/procedure/', ProcedureCreate.as_view(), name ='create-procedure'),
    path('reg/appointment/', AppointmentCreate.as_view(), name ='create-appointment'),
    path('reg/schedule/', ScheduleCreate.as_view(), name ='create-schedule'),
    path('reg/dayoff/', DayOffCreate.as_view(), name ='create-dayoff'),
    path('reg/user/', UserCreate.as_view(), name ='create-user'),
    path('reg/client/', ClientCreate.as_view(), name ='create-client'),

    #editar
    path('edit/procedure/<int:pk>/', ProcedureUpdate.as_view(), name ='edit-procedure'),
    path('edit/appointment/<int:pk>/', AppointmentUpdate.as_view(), name ='edit-appointment'),
    path('edit/schedule/<int:pk>/', ScheduleUpdate.as_view(), name ='edit-schedule'),
    path('edit/dayoff/<int:pk>/', DayOffUpdate.as_view(), name ='edit-dayoff'),
    path('edit/user/<int:pk>/', UserUpdate.as_view(), name ='edit-user'),
    path('edit/client/<int:pk>/', ClientUpdate.as_view(), name ='edit-client'),

    #deletar
    path('delete/procedure/<int:pk>/', ProcedureDelete.as_view(), name ='delete-procedure'),
    path('delete/appointment/<int:pk>/', AppointmentDelete.as_view(), name ='delete-appointment'),
    path('delete/schedule/<int:pk>/', ScheduleDelete.as_view(), name ='delete-schedule'),
    path('delete/dayoff/<int:pk>/', DayOffDelete.as_view(), name ='delete-dayoff'),
    path('delete/user/<int:pk>/', UserDelete.as_view(), name ='delete-user'),
    path('delete/client/<int:pk>/', ClientDelete.as_view(), name ='delete-client'),

    #listar
    path('list/procedure/', ProcedureList.as_view(), name ='list-procedure'),
    path('list/appointment/', AppointmentList.as_view(), name ='list-appointment'),
    path('list/schedule/', ScheduleList.as_view(), name ='list-schedule'),
    path('list/dayoff/', DayOffList.as_view(), name ='list-dayoff'),
    path('list/users/', UserList.as_view(), name ='list-user'),
    path('list/client/', ClientList.as_view(), name ='list-client'),

]