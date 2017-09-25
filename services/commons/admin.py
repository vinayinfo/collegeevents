from django.contrib import admin

from services.commons.models import UserParticipate


class UserParticipateAdmin(admin.ModelAdmin):
    model = UserParticipate
    list_display = ('user','content_type', 'object_id', 'status',)


admin.site.register(UserParticipate, UserParticipateAdmin)
