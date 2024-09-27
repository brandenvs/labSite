from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from .models import UserProfile

app_label = 'user_auth'

def get_theme(request):
    try:
        selected_theme = request.session['selected_theme']
    except:
        request.session.setdefault('selected_theme', 'light')
    
    selected_theme = request.session['selected_theme']
    if selected_theme:
        return HttpResponse(request.session['selected_theme'])

    else:
        request.session.setdefault('selected_theme', 'light')
        return HttpResponse(request.session['selected_theme'])

def toggle_theme(request):
    selected_theme = str(request.session['selected_theme'])
    
    if selected_theme:
        if selected_theme == 'light':
            request.session['selected_theme']  = 'dark'

        elif selected_theme == 'dark':
            request.session['selected_theme']  = 'light'
    
        return HttpResponse(request.session['selected_theme'])

    else:
        selected_theme = get_theme(request)
        return HttpResponse(request.session['selected_theme'])

def user_login(request):    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('portal:index'), {'message': 'You are already logged in!'})
    else:
        return render(request, 'authentication/login.html')

def create_new_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        print("User is trying to create a NEW USER while still logged in...")
        return render(request, 'authentication/sign_up.html', {'current_user': current_user})

    if request.method == 'POST':
        # Fetch User Details from Web Page
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        
        email_address = request.POST.get('emailaddress') 
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        print(password, confirm_password)
        
        if User.objects.filter(username=username).exists():
            return render(request, 'authentication/sign_up.html', {'message': 'Username already exists!'})
        elif password != confirm_password:
            return render(request, 'authentication/sign_up.html', {'message': 'Passwords do not match!'})
        elif User.objects.filter(email=email_address).exists():
            return render(request, 'authentication/sign_up.html', {'message': "Email address already associated to an account!"})
            

        try:
            # Create a New User instance and Set Attributes
            new_user = User.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                username=username, 
                email=email_address, 
                password=password
            )

            # Set Firstname
            new_user.first_name = first_name
            # Set Is? - Staff
            new_user.is_staff = False
            # Set Is? - Superuser
            new_user.is_superuser = False
            # Save User to Database
            new_user.save()
            
            # Associate user profile object
            UserProfile.objects.create(user=new_user)
            
            print("Successfully Added New User to Database")
            

            # Redirect User to Profile
            return render(request, 'authentication/login.html', {'success_message': 'User successfully created! Please login using the same credentials.'})

        # Catch the exception
        except Exception as ex:            
            # Get the Error Message
            error_message = str(ex)
            # Render Create User View and, Pass the Error Message to View
            return render(request, 'authentication/sign_up.html', {'message': error_message})

    # Render Initial Create User View
    return render(request, 'authentication/sign_up.html')

# Create User Function(Redirects...)
def user_create(request):
    if request.method == 'POST':
        # Get User Details from Web Page
        first_name = request.POST.get('firstname')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Create a New User & Save to Database
        try:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.is_staff = False
            user.is_superuser = False
            # Save user to Db
            user.save()
            # Redirect user
            return HttpResponseRedirect(reverse('portal:index'))
        except Exception as ex:
            print(f'SOMETHING WENT WRONG!\nError:\n{str(ex)}')
            return render(request, 'authentication/user_create.html', {'error': str(ex)})
    # Redirect User - create_new_user
    return HttpResponseRedirect(reverse('user_auth:create_new_user'))

# Create User View
def create_user(request):
    # Render View
    return render(request, 'authentication/sign_up.html')

# Login User(Authentication) Function - Handles Login Logic.
def authenticate_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    try:
        # Authorize user
        user = authenticate(username=username, password=password)

    except Exception as ex:
        print(ex)
        return HttpResponseRedirect(reverse('user_auth:login'), {'message': ex})

    # Handle invalid inputs
    if user is None:
        error_message = "Invalid Username or Password!"
        return render(request, 'authentication/login.html', {'message': error_message})
    else:
        # Login user 
        login(request, user)
        return HttpResponseRedirect(reverse('portal:index'))

# Renders View & Model - User Profile NOTE: Needs to be overhauled
def show_user(request):
    print(request.user.username)
    if request.user.is_authenticated:
        return render(request, 'authentication/user.html', {
            "username": request.user.username,
            "password": request.user.password,
            "firstname": request.user.first_name })
    else:
        return HttpResponseRedirect(reverse('user_auth:login'))

# Remove the authenticated user's ID from the request and flush their session data
def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse('user_auth:login'))
