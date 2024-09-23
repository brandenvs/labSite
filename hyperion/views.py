from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service import main

app_label = 'hyperion'

def get_service(request):
    response_code = main()
    
    if response_code == 200:
        return HttpResponseRedirect(reverse('hyperion:hd_home'))

def index(request):    
    if request.user.is_authenticated:      
        return render(request, 'hd_home.html')
    else:
        return HttpResponseRedirect(reverse('user_auth:login'))

