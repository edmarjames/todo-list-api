from django.shortcuts import render

from json import JSONDecodeError
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import views, status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from . serializers import RegistrationSerializer


class RegisterAPIView(views.APIView):

    serializer_class = RegistrationSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = RegistrationSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                auth_token = Token.objects.get(user=user).key

                data = {
                    'message': 'Successfully registered a new user!',
                    'token': auth_token
                }

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)