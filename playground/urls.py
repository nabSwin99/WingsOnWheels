from django.urls import path
from .import views
from django.urls import path
from .views import generate_and_display_map, add_to_cart,view_cart, update_cart

# URLConf
urlpatterns = [
path('', views.home),
path('order', views.order, name='order'),
path('signin_home', views.signin_home, name='signin_home'),
path('show-map/', generate_and_display_map, name='show_map'),
path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
path('view_cart', view_cart, name='view_cart'),
path('update-cart/<int:item_id>/<str:action>/', update_cart, name='update_cart'),
path('confirm-order', views.confirm_order, name='confirm_order'),
path('show-map/order_delivered', views.order_delivered, name='order_delivered'),
]
