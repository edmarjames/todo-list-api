# import dependency from rest_framework
from rest_framework import serializers, status
from rest_framework.fields import CharField, DateField
from rest_framework.exceptions import APIException, ValidationError

# import needed models
from django.contrib.auth.models import User
from . models import Task

from collections import OrderedDict
from datetime import datetime, date


# custom serializer to remove leading and trailing commas on CharFields
class StrippedCharField(serializers.CharField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().to_internal_value(data)

# custom serializer to remove leading and trailing commas on DateFields
class StrippedDateField(serializers.DateField):
    default_format = '%Y-%m-%d'

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().to_internal_value(data)

    def to_representation(self, value):
        if isinstance(value, date):
            return value.strftime(self.default_format)
        return value


class RegistrationSerializer(serializers.ModelSerializer):

    # define validations on fields. The write-only fields means that it is accepted during POST requests, but it will not be included in GET requests.
    username = StrippedCharField(required=True)
    email = StrippedCharField(required=True)
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

        return user


class DateIsInPastException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Deadline cannot be in the past'
    default_code = 'invalid'


class TaskSerializer(serializers.ModelSerializer):

    # user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), many=False, read_only=True)
    user = serializers.ReadOnlyField(source='user.username', required=False)
    title = StrippedCharField(required=True)
    description = StrippedCharField(required=True)
    status = StrippedCharField(required=False)
    deadline = StrippedDateField(required=True)
    date_created = StrippedDateField(required=False)

    class Meta:
        model = Task
        fields = ('title', 'description', 'status',
                  'deadline', 'date_created', 'user', 'is_active')
        read_only_fields = ('user',)

    def validate(self, res: OrderedDict):
        current_date = datetime.now().date()
        deadline = res.get("deadline")

        if deadline and deadline < current_date:
            raise DateIsInPastException
        return res

    def save(self):

        title = self.validated_data['title']
        all_titles = Task.objects.values_list('title', flat=True)

        for titles in all_titles:
            if title == titles:
                raise serializers.ValidationError(
                    {'title': 'Operation failed, there is an existing task with the same title.'})

        task = Task(
            description=self.validated_data['description'],
            deadline=self.validated_data['deadline'],
            title=title,
            user=self.validated_data['user']
        )

        task.save()

    def update(self, instance, validated_data):

        title = validated_data.get('title', instance.title)
        description = validated_data.get('description', instance.description)
        status = validated_data.get('status', instance.status)
        deadline = validated_data.get('deadline', instance.deadline)

        if Task.objects.filter(title=title).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(
                {'title': 'Operation failed, there is an existing task with the same title.'})

        instance.title = title
        instance.description = description
        instance.status = status
        instance.deadline = deadline
        instance.save()

        return instance
