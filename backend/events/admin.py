from django.contrib import admin
from .models import Event, ABTestVisit


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'location', 'source')
    search_fields = ('title', 'description', 'location', 'source')
    list_filter = ('source',)


@admin.register(ABTestVisit)
class ABTestVisitAdmin(admin.ModelAdmin):
    list_display = ('variant', 'session_key', 'visited_at', 'ip_address')
    list_filter = ('variant', 'visited_at')
    search_fields = ('session_key', 'ip_address')
    readonly_fields = ('session_key', 'variant', 'visited_at', 'ip_address', 'user_agent')
