from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_auth.urls')),
    path('hyperion/', include('hyperion.urls')),
    path('portal/', include('portal.urls')),
]
