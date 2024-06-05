from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from accounts.models import Customer
from django.db import transaction
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError


# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("login")
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        state = request.POST['state']
        postcode =request.POST['postcode']
        suburb = request.POST['suburb']
        street_address = request.POST['street_address']

        state_mappings = {
            'VIC': [3, 8],
        }
        # Extract the first digit of the postcode
        postcode_first_digit = int(postcode[0])
        if postcode_first_digit in state_mappings[state]:
                # Postcode matches the state, so it's valid
                postcode =request.POST['postcode']
        else:
                # Postcode does not match the state, so it's invalid
                messages.info(request, "Postcode doesn't match provided State!")
                return redirect('register')
        # Validate address using Nominatim
        locator = Nominatim(user_agent="myapp")
        full_address = f"{street_address}, {suburb}, {state}, {postcode}, Australia"
        try:
            location = locator.geocode(full_address)
            if not location:
                messages.info(request, "Invalid address. Please enter a valid address in Victoria.")
                return redirect('register')
        except GeocoderServiceError as e:
            messages.info(request, f"Geocoding service error: {e}")
            return redirect('register')


        # Concatenating address components into one field
        address = f"{street_address}, {suburb}, {state}, {postcode}, Australia"

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken!")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already In Use!")
                return redirect('register')
            else:
                with transaction.atomic():
                    user = User.objects.create_user( username= username, password=password2, first_name=first_name, last_name=last_name, email=email)
                    user.save()
                    customer = Customer(user=user, phone=phone, address=address)
                    customer.save()
                    messages.success(request, "Registration successful")
                    return redirect('login')
        
        else:
            messages.info(request, "Password Not Matching!")
            return redirect('register')
    else:
        return render(request, 'register.html')

