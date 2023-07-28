from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('login/', auth_views.LoginView.as_view(
        template_name = 'users/form.html',
    ), name ='login'),
        path('loginn/', auth_views.LoginView.as_view(
        template_name = 'users/loginn.html',
    ), name ='loginn'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),

]