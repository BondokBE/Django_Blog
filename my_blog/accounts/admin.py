from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

class ProfileModelAdmin(admin.ModelAdmin):
    fullname = f"{User.first_name} {User.last_name}"
    list_display = ["user", "job_title", "bio"]
    search_fields = ["user"]
    
    class Meta:
        model = Profile


admin.site.register(Profile, ProfileModelAdmin)