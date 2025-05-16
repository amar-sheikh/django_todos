from django.db import models

class Todo(models.Model):
    task_name=models.CharField(max_length=50)
    task_description=models.TextField(null=True, blank=True)
    is_completed=models.BooleanField(default=False)

    def __str__(self):
        return self.task_name