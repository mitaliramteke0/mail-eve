from django.http import JsonResponse
from django.core.mail import EmailMessage
from .tasks import send_event_reminder_emails_task  # Import your Celery task
from celery.exceptions import CeleryError  # Import CeleryError
from .models import Event, EventTemplate, Employee, EmailLog, LastExecution
from datetime import date, datetime



def retrieve_event_data(request):
    """
    API endpoint to retrieve event data for the current date.
    """
    today = date.today()
    current_events = Event.objects.filter(event_date=today)
    print(current_events)
    event_data = []
    for event in current_events:
        event_data.append({
            "employee_name": event.employee.name,
            "employee_email": event.employee.email,
            "event_type": event.event_type,
            "event_date": event.event_date.strftime("%Y-%m-%d"),
        })
    # Check if there are events for the current date
    if not event_data:
        return JsonResponse({"message": "No events for the current date."})
    
    return JsonResponse({"events": event_data})

def send_event_reminder_emails_view(request):
    """
    API endpoint to trigger sending event reminder emails asynchronously using Celery.
    """
    try:
        send_event_reminder_emails_task.delay()  # Queue the Celery task
        return JsonResponse({"message": "Email sending task is queued."})
    except CeleryError as e:
        return JsonResponse({"error": "Failed to queue the email sending task.", "detail": str(e)})


def process_events_and_send_emails(request):
    """
    API endpoint to process events, send personalized emails, and log email sending status.
    """
    today = date.today()
    current_events = Event.objects.filter(event_date=today)

    for event in current_events:
        try:
            # Retrieve the event template based on event type
            template = EventTemplate.objects.get(event_type=event.event_type)
            
            # Populate the email template with member details and event-specific content
            subject = f"Reminder: {event.event_type}"
            message = template.template_content.format(employee=event.employee.name)
            
            # Send the personalized email to the employee's email address
            email = EmailMessage(subject, message, to=[event.employee.email])
            email.send()
            
            # Log successful email sending
            EmailLog.objects.create(
                employee=event.employee,
                event=event,
                status="Sent",
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
            )

    # Update the last successful execution time
    try:
        last_execution, created = LastExecution.objects.get_or_create(id=1)
        last_execution.last_successful_execution_time = datetime.now()
        last_execution.save()
    except Exception as e:
        # Handle any errors that may occur while updating the time
        pass

    return JsonResponse({"message": "Email processing task is completed."})


def view_email_logs(request):
    """
    API endpoint to view email sending logs.
    """
    email_logs = EmailLog.objects.all()
    logs_data = []

    for log in email_logs:
        logs_data.append({
            "employee_name": log.employee.name,
            "event_type": log.event.event_type,
            "status": log.status,
            "sent_datetime": log.sent_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "error_message": log.error_message if log.error_message else "",
        })

    return JsonResponse({"email_logs": logs_data})
