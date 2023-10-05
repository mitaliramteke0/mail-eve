from celery import shared_task
from django.utils import timezone
from .models import Event, EventTemplate, EmailLog
from django.core.mail import EmailMessage
from datetime import date

@shared_task
def send_event_reminder_emails_task():
    """
    Celery task to send event reminder emails asynchronously.
    """
    today = date.today()
    current_events = Event.objects.filter(event_date=today)

    for event in current_events:
        try:
            template = EventTemplate.objects.get(event_type=event.event_type)
            subject = f"Reminder: {event.event_type}"
            message = template.template_content.format(employee=event.employee.name)
            email = EmailMessage(subject, message, to=[event.employee.email])
            email.send()
            # Log successful email sending
            EmailLog.objects.create(
                employee=event.employee,
                event=event,
                status="Sent",
                sent_datetime=timezone.now()
            )
        except EventTemplate.DoesNotExist:
            # Handle the case where no template is found for the event type.
            pass
        except Exception as e:
            # Log the error message if email sending fails
            EmailLog.objects.create(
                employee=event.employee,
                event=event,
                status="Error",
                error_message=str(e),
                sent_datetime=timezone.now()
            )
