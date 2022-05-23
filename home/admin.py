from django.contrib import admin
from .models import Post

# Register your models here.
# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','created')
    search_fields = ('user','slug')
    list_filter=('user','slug')
    prepopulated_fields={'slug':('body',)}

