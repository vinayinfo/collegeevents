from django.contrib import admin

from services.feeds.models import Feed


# Register your models here.
class FeedAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'object_id', 'parent', 'message')
    list_filter = ('content_type', 'created_at')

admin.site.register(Feed, FeedAdmin)
