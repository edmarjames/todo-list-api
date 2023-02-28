# import dependency from rest_framework
from rest_framework                 import serializers

# import needed models
from django.contrib.auth.models     import User


# custom serializer to remove leading and trailing commas on fields
class StrippedCharField(serializers.CharField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().to_internal_value(data)

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
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    # override the save method
    def save(self):
        # creates a new User instance and populates the username, email, first_name and last_name fields from the validated data
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name']
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