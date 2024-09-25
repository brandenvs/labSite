from django.urls import path
from . import views

# Define WebApplication Name
app_name = 'user_auth'

# Define URL patterns - (app)'user-auth'
urlpatterns = [
    # URL Pattern - User Login
    path('', views.user_login, name='login'),
    # URL Pattern - Create New User
    path('create-user/', views.create_user, name='create_user'),# NOTE RE-ROUTED TO LOGIN
    # URL Pattern - POST Create New User
    path('create-new-user/', views.create_new_user, name='create_new_user'), # NOTE RE-ROUTED TO LOGIN
    # URL Pattern - Authenticate users
    path('authenticate-user/', views.authenticate_user, name='authenticate_user'),
    # URL Pattern - Show user details
    path('show-user/', views.show_user, name='show_user'),
    # URL Pattern - Logout user
    path('logout-user/', views.logout_user, name='logout_user'),
    # Theme toggler
    path('toggle-theme/', views.toggle_theme, name='toggle_theme')
]
