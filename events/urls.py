from django.urls import path
from . import views

urlpatterns = [
    # Define API endpoints for events app
    path('retrieve-event-data/', views.retrieve_event_data, name='retrieve_event_data'),
    path('view-email-logs/', views.view_email_logs, name='view_email_logs'),
    path('process-events-and-send-emails/', views.process_events_and_send_emails, name='process_events_and_send_emails'),
    path('send-event-reminder-emails/', views.send_event_reminder_emails_view, name='send_event_reminder_emails'),

]
