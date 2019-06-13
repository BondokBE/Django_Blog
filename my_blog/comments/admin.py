from django.contrib import admin
from .models import Comment

# Register your models here.

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["user", "content", "time_stamp", "id"]
    list_display_links = ["user", "content"]
    list_filter = ["user", "time_stamp"]
    search_fields = ["user", "content", "time_stamp"]

    class Meta:
        model = Comment

admin.site.register(Comment, CommentModelAdmin)
