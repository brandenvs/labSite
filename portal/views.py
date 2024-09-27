from django.shortcuts import render
from django.contrib.auth.decorators import login_required

app_label = 'portal'

@login_required(login_url='user_auth:login')
def index(request):
    return render(request, 'portal.html')

def waka_time(request):
    pass
