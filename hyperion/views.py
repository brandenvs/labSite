from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service import main

app_label = 'hyperion'

def get_service(request):
    response_code = main()
    
    if response_code == 200:
        return render(request, 'index.html', {'message': 'wait(10)', 'response': response_code})

def index(request):    
    if request.user.is_authenticated:      
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect(reverse('user_auth:login'))

