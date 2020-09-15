from django.contrib import admin
from .models import SocialUser

class SocialUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'university')

admin.site.register(SocialUser, SocialUserAdmin)
