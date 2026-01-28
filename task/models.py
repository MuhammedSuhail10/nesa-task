from django.db import models
from user.models import User

class Task(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to_user')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('progress', 'In Progress'), ('completed', 'Completed')], default='pending')
    report = models.TextField(null=True, blank=True)
    worked_hour = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title