from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Site hubs and security
    path('admin/', admin.site.urls),
    path('old-auth/', include('user_auth.urls')),
    path('', include('users.urls')), # New

    path('portal/', include('portal.urls')),

    # Applications
    path('hd-v00/', include('hyperion.urls')),
    path('fr-v00/', include('hyperion.urls')),
    path('sbg-trade-v00/', include('hyperion.urls')),
    
]
