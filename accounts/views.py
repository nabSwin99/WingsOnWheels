from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from accounts.models import Customer
from django.db import transaction


# Create your views here.

def signin_home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/order")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("login")
    else:
        return render(request, 'signin_home.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

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



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        address = request.POST['address']

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
                    return redirect('login')
                
        
        
        else:
            messages.info(request, "Password Not Matching!")
            return redirect('register')


    else:
        return render(request, 'register.html')
