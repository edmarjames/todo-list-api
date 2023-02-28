from rest_framework import serializers
from rest_framework.fields import CharField
from django.contrib.auth.models import User


class StrippedCharField(serializers.CharField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = data.strip()
        return super().to_internal_value(data)

class RegistrationSerializer(serializers.ModelSerializer):

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
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def save(self):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({
                'password': 'Sorry, the password did not match'
            })

        user.set_password(password)

        user.save()

        return user