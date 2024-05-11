from django.shortcuts import render
from django.http import HttpResponse
from .map_optimizer import generate_route_map, save_map

# Create your views here.

def home(request):
    return render(request, 'homepage.html')

def order(request):
    return render(request, 'order.html')

def signin_home(request):
    return render(request, 'signin_home.html')


def generate_and_display_map(request):
    # Generate the map
    route_map = generate_route_map()
    # Save the map to a file (could also serve directly from memory)
    filename = save_map(route_map)

    # Serve the HTML file content
    with open(filename, 'r') as file:
        return HttpResponse(file.read(), content_type='text/html')