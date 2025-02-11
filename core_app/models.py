from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    task = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task} - {'Completed' if self.completed else 'Pending'}"