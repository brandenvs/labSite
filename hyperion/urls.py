from django.urls import path
from . import views

# Define webapp name
app_name = 'hyperion'

urlpatterns = [
    path('', views.index, name='index'),
    path('service/', views.get_service, name='student_tracker')
]