from django.urls import path
from . import views

# Define WebApplication Name
app_name = 'user_auth'

# Define URL patterns - (app)'user_auth'
urlpatterns = [
    # URL Pattern - User Login
    path('', views.user_login, name='login'),
    # URL Pattern - Create New User
    path('create_user/', views.create_user, name='create_user'),
    # URL Pattern - POST Create New User
    path('create_new_user/', views.create_new_user, name='create_new_user'),
    # URL Pattern - Authenticate users
    path('authenticate_user/', views.authenticate_user, name='authenticate_user'),
    # URL Pattern - Show user details
    path('show_user/', views.show_user, name='show_user'),
    # URL Pattern - Logout user
    path('logout_user/', views.logout_user, name='logout_user')
]



