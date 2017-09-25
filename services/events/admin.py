from django.contrib import admin

from services.events.models import Events


class EventsAdmin(admin.ModelAdmin):
    model = Events
    list_display = ('name',)


admin.site.register(Events, EventsAdmin)
