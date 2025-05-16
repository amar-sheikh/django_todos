from django.db import models
from django.core.validators import MinLengthValidator

class Todo(models.Model):
    task_name=models.CharField(max_length=50, unique=True, null=False, validators=[MinLengthValidator(3)])
    task_description=models.TextField(null=True, blank=True)
    is_completed=models.BooleanField(default=False)

    def __str__(self):
        return self.task_name