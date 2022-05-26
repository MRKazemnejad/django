from django.contrib import admin
from .models import Post,Relation,Comment

# Register your models here.
# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','created')
    search_fields = ('user','slug')
    list_filter=('user','slug')
    prepopulated_fields={'slug':('body',)}

admin.site.register(Relation)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user','body','is_replay','post')
    raw_id_fields=('user','post','replay')