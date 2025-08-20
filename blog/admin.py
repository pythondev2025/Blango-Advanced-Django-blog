from django.contrib import admin
from .models import Tag, Post, Comment, AuthorProfile


class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("title",)}
  list_display = ("title", "slug", "published_at")


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(AuthorProfile)
