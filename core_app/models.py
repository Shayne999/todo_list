from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'PENDING'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('COMPLETED', 'COMPLETED')
    ], default='PENDING')
    date_created = models.DateTimeField(auto_now_add=True)
    due_date = models.CharField(null=True, blank=True)

    def __str__(self):
        return self.title