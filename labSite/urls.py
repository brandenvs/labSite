from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('user_auth.urls')),
    path('hyperion/', include('hyperion.urls'))
    
]
