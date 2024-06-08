from django.shortcuts import render
from django.http import HttpResponse
import json

from .map_optimizer import generate_route_map , create_map_html
from .models import MenuItem, Order, OrderItem
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def add_to_cart(request, item_id):
    print("Session before modification:", request.session.get('cart', {}))
    
    item = get_object_or_404(MenuItem, pk=item_id)
    cart = request.session.get('cart', {})
    item_key = str(item_id)

    if item_key in cart:
        cart[item_key] += 1
    else:
        cart[item_key] = 1

    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({'message': f'Added {item.name} to cart'})



# Create your views here.

def home(request):
    return render(request, 'homepage.html')

def order(request):
    items = MenuItem.objects.all()  # Retrieves all items from the database
    return render(request, 'order.html', {'items': items})

def signin_home(request):
    return render(request, 'signin_home.html')


def generate_and_display_map(request):
    # Generate the map
    route_map = generate_route_map(request)

    filename = 'route_map.html'
    start_location = "593 Glenferrie Rd, Hawthorn VIC 3122"
    end_location = request.user.customer.address

    order_id = request.session.get('order_id', None)
    if order_id is not None:
        order = Order.objects.get(id=order_id)

        cart = request.session.get('cart', {})
        items = []
        total_price = 0
        for item_id, quantity in cart.items():
            item = MenuItem.objects.get(id=item_id)
            item_total = item.price * quantity
            total_price += item_total
            items.append({
                'name': item.name,
                'price': str(item.price),
                'quantity': quantity,
                'total': str(item_total),
                })
        cart_details = {
            'items': items,
            'total_price': str(total_price)  
            }       
        cart_details_json = json.dumps(cart_details)
                    

        # You can now use 'order' to access order details and pass them to the template
        create_map_html(request, filename, start_location, end_location, order, cart_details_json)
    else:
        # Handle cases where there is no order ID found, maybe redirect or show error
        return render(request, 'view_cart.html') # Redirect back to cart

    # Clear the cart
    request.session['cart'] = {}

    # Serve the HTML file content
    with open(filename, 'r') as file:
        return HttpResponse(file.read(), content_type='text/html')
    

def order_delivered(request):
    order_id = request.session.get('order_id', None)
    order = Order.objects.get(id=order_id)  # Retrieve the order by ID or other criteria
    # Chaning delivery status in database.
    order.set_delivered()
    return redirect('/')


    
def view_cart(request):
    cart = request.session.get('cart', {})
    items = MenuItem.objects.filter(id__in=cart.keys())
    cart_items = [(item, cart[str(item.id)]) for item in items]
    total_price = sum(item.price * quantity for item, quantity in cart_items)
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

def update_cart(request, item_id, action):
    cart = request.session.get('cart', {})
    item_key = str(item_id)
    
    if action == 'add':
        cart[item_key] = cart.get(item_key, 0) + 1
    elif action == 'remove':
        if cart.get(item_key, 0) > 1:
            cart[item_key] -= 1
        else:
            cart.pop(item_key, None)
    
    request.session['cart'] = cart
    return JsonResponse({'success': True})


@login_required
def confirm_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return render(request, 'view_cart.html')  #  to inform the user the cart is empty

        order = Order(customer=request.user)
        order.save()  # The status will automatically be 'Pending'

        for item_id, quantity in cart.items():
            item = MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=quantity)

        
        request.session['order_id'] = order.id  # Save order ID in session for use in the next view

        return redirect('show-map/')  # Redirect to a new URL for order success page

    return render(request, 'view_cart.html')  # Show the cart if not a POST request


## Functions for showing about and FAQ pages.
def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related('orderitem_set__item')
    orders_with_totals = []
    for order in orders:
        total = sum(orderitem.item.price * orderitem.quantity for orderitem in order.orderitem_set.all())
        orders_with_totals.append({
            'order': order,
            'total': total
        })
    
    context = {
        'orders_with_totals': orders_with_totals,
    }
    return render(request, 'order_history.html', context)