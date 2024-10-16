from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .service import main

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
    with open('portfolio_links.txt', 'a') as file:
        url = request.POST.get('link')
        file.write('\n' + url)

    return HttpResponseRedirect(reverse('hyperion:hd_home'))

def delete_port(request):
    if request.method == 'POST':
        _student = dbStudent.objects.filter(fullname=request.POST.get('fullname'))
        _student.delete()

    return HttpResponseRedirect(reverse('hyperion:hd_home'))
