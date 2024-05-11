from django.urls import path
from .import views


# URLConf
urlpatterns = [

path('register', views.register, name='register'),
path('login', views.login, name='login'),
path('logout', views.logout, name='logout'),
path('signin_home', views.signin_home, name='signin_home')

]
