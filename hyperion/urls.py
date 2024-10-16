from django.urls import path
from . import views

# Define webapp name
app_name = 'hyperion'

urlpatterns = [
    path('', views.index, name='hd_home'),
    path('service/', views.get_service, name='student_tracker'),
    path('add-portfolio/', views.add_port, name='add_port')
    
    
]