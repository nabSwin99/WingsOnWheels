from django.urls import path
from .import views
from django.urls import path
from .views import generate_and_display_map

# URLConf
urlpatterns = [
path('', views.home),
path('order', views.order, name='order'),
path('signin_home', views.signin_home, name='signin_home'),
path('show-map/', generate_and_display_map, name='show_map'),


]
