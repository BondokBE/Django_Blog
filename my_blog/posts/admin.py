from django.contrib import admin
from .models import Post

# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "updated", "time_stamp"]
    list_display_links = ["updated"]
    list_filter = ["title", "updated"]
    search_fields = ["title", "content"]
    list_editable = ["title"]
    # ordering = ["title"] # to choose the default  order 
    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)


