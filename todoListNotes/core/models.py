# import models
from django.db                      import models
# import User model
from django.contrib.auth.models     import User
# import datetime
import datetime

# import abstract class from utils
from utils.model_abstracts          import Model
# import abstract classes
from django_extensions.db.models    import (TimeStampedModel, TitleDescriptionModel)


# custom abstract class for 'is_active' field
class CustomActivatorModel(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

# Task model that inherits abstract model classes
class Task(
    TimeStampedModel,
    TitleDescriptionModel,
    CustomActivatorModel,
    Model
    ):

    class Meta:
        # verbose_name for single object
        verbose_name = "Task"
        # verbose_name for multiple objects
        verbose_name_plural = "Tasks"
        # default ordering
        ordering = ["id"]

    # additional fields
    status = models.CharField(max_length=50, default='Pending')
    deadline = models.DateField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=False)

    # generate string representation
    def __str__(self):
        return f'{self.title} {self.description}'
    

# Note model that inherits abstract model classes
class Note(
    TimeStampedModel,
    TitleDescriptionModel,
    Model
    ):

    class Meta:
        # verbose_name for single object
        verbose_name =  "Note"
        # verbose_name for multiple objects
        verbose_name_plural = "Notes"
        # default ordering
        ordering = ["id"]

    # additional fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=False)

    # generate string representation
    def __str__(self):
        return f'{self.title} {self.description}'

