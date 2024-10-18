from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    
    path('fetch-theme/', views.get_theme, name='get_theme'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    
]
