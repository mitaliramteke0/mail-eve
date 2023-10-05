from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Event(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    event_date = models.DateField()

class EventTemplate(models.Model):
    event_type = models.CharField(max_length=50, unique=True)
    template_content = models.TextField()

class EmailLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True, null=True)
    sent_datetime = models.DateTimeField(auto_now_add=True)

class LastExecution(models.Model):
    last_successful_execution_time = models.DateTimeField()

    def __str__(self):
        return str(self.last_successful_execution_time)