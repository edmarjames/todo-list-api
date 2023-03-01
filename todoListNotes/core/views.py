from django.shortcuts import render

from json import JSONDecodeError
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import views, viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)

from . serializers import RegistrationSerializer, TaskSerializer
from . models import Task

from datetime                       import datetime, date

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
        
class TaskViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet
    ):

    permission_classes = (IsAuthenticated,)
    # authentication_classes = [TokenAuthentication]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user = user)

    def create(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = TaskSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.validated_data['user'] = request.user
                serializer.save()

                result = {
                    'message': 'Successfully added a new task',
                    'details': serializer.data
                }

                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
        
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            data = JSONParser().parse(request)
            serializer = self.get_serializer(instance, data=data, partial=partial)

            if serializer.is_valid(raise_exception=True):
                # self.perform_update(serializer)
                serializer.update(instance, serializer.validated_data)

                result = {
                    'message': 'Task successfully updated',
                    'details': serializer.data
                }

                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
        
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            result = {
                "message": "Task successfully deleted",
            }

            return Response(result, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
