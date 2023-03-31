# import dependencies from rest_framework
from rest_framework                 import serializers, status
from rest_framework.exceptions      import APIException

# import needed models
from django.contrib.auth.models     import User
from . models                       import Task, Note

# import OrderedDict
from collections                    import OrderedDict

# import date dependencies
from datetime                       import datetime, date

# import re for regex
import re

# import EmailField and validate_email
from django.core.validators         import validate_email
from django.forms import            EmailField


# custom serializer to remove leading and trailing whitespace, period and comma on CharFields
class StrippedCharField(serializers.CharField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = re.sub(r'^[\s,\.]+|[\s,\.]+$', '', data.strip())
        return super().to_internal_value(data)


# custom serializer to remove leading and trailing whitespace, period and comma on DateFields
class StrippedDateField(serializers.DateField):
    default_format = '%Y-%m-%d'
    pattern = r'^[\s,\.]+|[\s,\.]+$'

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = re.sub(self.pattern, '', data.strip())
        return super().to_internal_value(data)

    def to_representation(self, value):
        if isinstance(value, date):
            return value.strftime(self.default_format)
        return value


# custom serializer to remove leading and trailing whitespace, period and comma on EmailField while still using the email validation
class StrippedEmailField(EmailField):
    def to_python(self, value):
        value = value.strip('., \t\n\r')  # strip leading and trailing period, comma, and whitespace
        value = super().to_python(value)  # use the built-in EmailField validation
        return value


# custom exception if the deadline date is in the past
class DateIsInPastException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Deadline cannot be in the past'
    default_code = 'invalid'


# serializer for Registration
class RegistrationSerializer(serializers.ModelSerializer):

    # define validations on fields. The write-only fields means that it is accepted during POST requests, but it will not be included in GET requests.
    username = StrippedCharField(required=True)
    email = StrippedEmailField(required=True)
    first_name = StrippedCharField(required=True)
    last_name = StrippedCharField(required=True)
    password = StrippedCharField(write_only=True, required=True)
    password2 = StrippedCharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True
    )

    class Meta:
        # define model
        model = User
        # define the fields to be serialize/deserialize
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password', 'password2']

    # override the save method
    def save(self):
        # creates a new User instance and populates the username, email, first_name and last_name fields from the validated data
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )

        # get the validated data and store it to variables
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # It then validates that the password and password2 fields match.
        if password != password2:
            raise serializers.ValidationError({
                'password': 'Sorry, the password did not match'
            })

        # If they do, it sets the password using user.set_password(password)
        user.set_password(password)

        # saves the user using user.save()
        user.save()

        # return the saved user
        return user


# serializer for Task
class TaskSerializer(serializers.ModelSerializer):

    # declare user as read-only so that it is not required during deserialization
    user = serializers.ReadOnlyField(source='user.username', required=False)
    title = StrippedCharField(required=True)
    description = StrippedCharField(required=True)
    status = StrippedCharField(required=False)
    deadline = StrippedDateField(required=True)
    color = StrippedCharField(required=True)

    class Meta:
        # define model
        model = Task
        # define the fields to be serialize/deserialize
        fields = ['title', 'description', 'status',
                  'deadline', 'color', 'created', 'modified', 'user', 'is_active']
        read_only_fields = ('user',)

    # override the validate method
    def validate(self, res: OrderedDict):
        # get current date
        current_date = datetime.now().date()
        # get the deadline from request body
        deadline = res.get("deadline")

        # if deadline is not None and deadline less than the current date
        if deadline and deadline < current_date:
            # raise an exception
            raise DateIsInPastException
        return res

    # override the save method
    def save(self):
        # get the 'title' validated data
        title = self.validated_data['title']
        # get all titles from Task model
        all_titles = Task.objects.values_list('title', flat=True)

        # loop through the all_titles list
        for titles in all_titles:
            # if the title is already existing
            if title == titles:
                # raise a ValidationError
                raise serializers.ValidationError(
                    {'title': 'Operation failed, there is an existing task with the same title.'})

        # create the task instance and populate the fields
        task = Task(
            title=title,
            description=self.validated_data['description'],
            deadline=self.validated_data['deadline'],
            color=self.validated_data['color'],
            # gets the currently authenticated user
            user=self.validated_data['user']
        )

        # save the created task
        task.save()

    # override the update method
    def update(self, instance, validated_data):
        # get the fields you want to update
        title = validated_data.get('title', instance.title)
        description = validated_data.get('description', instance.description)
        status = validated_data.get('status', instance.status)
        deadline = validated_data.get('deadline', instance.deadline)
        color = validated_data.get('color', instance.color)

        # Check if there is a task with the same title, except for the current instance
        if Task.objects.filter(title=title).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(
                {'title': 'Operation failed, there is an existing task with the same title.'})

        # update the instance fields
        instance.title = title
        instance.description = description
        instance.status = status
        instance.deadline = deadline
        instance.color = color

        # save the instance
        instance.save()

        # return the updated instance
        return instance


# serializer for Note
class NoteSerializer(serializers.ModelSerializer):

    # declare user as read-only so that it is not required during deserialization
    title = StrippedCharField(required=True)
    content = StrippedCharField(source='description', required=True)
    user = serializers.ReadOnlyField(source='user.username', required=False)
    color = StrippedCharField(required=True)

    class Meta:
        # define mode
        model = Note
        # define the fields to be serialize/deserialize
        fields = ['title', 'content', 'color', 'created', 'modified', 'user']
        read_only_fields = ('user',)

    # override the save method
    def save(self):
        # get the 'title' validated data
        title = self.validated_data['title']
        # get all titles from Note model
        all_titles = Note.objects.values_list('title', flat=True)

        # loop through the all_titles list
        for titles in all_titles:
            # if the title is already existing
            if title == titles:
                # raise a ValidationError
                raise serializers.ValidationError({'title': 'Operation failed, there is an existing note with the same title.'})
            
        # create the note instance and populate the fields
        note = Note (
            title = title,
            description = self.validated_data['description'],
            color = self.validated_data['color'],
            user = self.validated_data['user']
        )

        # save the created note
        note.save()

    # override the update method
    def update(self, instance, validated_data):
        # get the fields you want to update
        title = validated_data.get('title', instance.title)
        description = validated_data.get('description', instance.description)
        color = validated_data.get('color', instance.color)

        # Check if there is a note with the same title, except for the current instance
        if Note.objects.filter(title=title).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'title', 'Operation failed, there is an existing note with the same title'})
        
        # update the instance fields
        instance.title = title
        instance.description = description
        instance.color = color

        # save the instance
        instance.save()

        # return the updated instance
        return instance
    

# serializer for user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # define model
        model = User
        # define the fields to be serialize/deserialize
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser']