from django.db import models
from django.contrib.auth.models import User
import datetime

from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleDescriptionModel
)


class Task(
    TimeStampedModel,
    ActivatorModel,
    TitleDescriptionModel,
    Model
    ):

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["id"]

    status = models.CharField(max_length=50, default='Pending')
    deadline = models.DateField(null=False, blank=False)
    date_created = models.DateField(default=datetime.date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title} {self.description}'
