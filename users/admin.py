from django.contrib import admin
from users.models import AstroProfile

class AstroProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'selected_theme')

admin.site.register(AstroProfile, AstroProfileAdmin)