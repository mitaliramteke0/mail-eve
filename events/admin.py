from django.contrib import admin
from .models import Employee, Event, EventTemplate, EmailLog

# Register the models to make them accessible in the admin interface

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)
    search_fields = ('name', 'email',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('employee', 'event_type', 'event_date',)
    list_filter = ('event_type', 'event_date',)
    search_fields = ('employee__name', 'event_type',)
    date_hierarchy = 'event_date'

@admin.register(EventTemplate)
class EventTemplateAdmin(admin.ModelAdmin):
    list_display = ('event_type',)
    search_fields = ('event_type',)

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'event', 'status', 'sent_datetime',)
    list_filter = ('status', 'sent_datetime',)
    search_fields = ('employee__name', 'event__event_type',)
    date_hierarchy = 'sent_datetime'
