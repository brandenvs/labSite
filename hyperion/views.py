from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service import main
import time
from .models import dbStudent

app_label = 'hyperion'

def get_service(request):
    response_code = main()
    
    if response_code == 200:
        return HttpResponseRedirect(reverse('hyperion:hd_home'))

def index(request):
    if request.user.is_authenticated:
        db_students = dbStudent.objects.all()

        return render(request, 'hd_home.html', {'db_students': db_students})

    else:
        return HttpResponseRedirect(reverse('user_auth:login'))

def add_port(request):
    if request.method == 'POST':
        portfolio_url=request.POST.get('link')
        
    # if dbStudent.objects.get(portfolio_url=portfolio_url):
    #     return render(request, 'hd_home.html', {'message': 'student'})

        
        dbStudent.objects.create(
            portfolio_url=request.POST.get('link')
        ).save()

    time.sleep(2)
    get_service(request)

    return HttpResponseRedirect(reverse('hyperion:hd_home'))

def delete_port(request):
    if request.method == 'POST':
        dbStudent.objects.filter(
            fullname=request.POST.get('fullname')
        ).delete()

    time.sleep(2)
    get_service(request)

    return HttpResponseRedirect(reverse('hyperion:hd_home'))
