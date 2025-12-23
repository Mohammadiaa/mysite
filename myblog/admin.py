from django.contrib import admin
from myblog.models import Post,Category
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    empty_value_display = "empty"
    list_display = ("title", "author" ,"counted_views", "status", "published_date")
    list_filter = ("status", "author")
    search_fields = ["title", "content"]

admin.site.register(Category)
admin.site.register(Post,  PostAdmin)
