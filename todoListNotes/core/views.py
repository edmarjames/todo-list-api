from django.shortcuts   import render

# import JSONDecodeError and JsonResponse
from json                               import JSONDecodeError
from django.http                        import JsonResponse

# import dependencies from rest_framework
from rest_framework.authtoken.models    import Token
from rest_framework.response            import Response
from rest_framework.parsers             import JSONParser
from rest_framework                     import views, viewsets, status
from rest_framework.decorators          import api_view, permission_classes
from rest_framework.permissions         import IsAuthenticated

# import mixins from rest_framework
from rest_framework.mixins              import (ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin)

# import needed serializers
from . serializers                      import RegistrationSerializer, TaskSerializer, NoteSerializer

# import needed model/s
from . models                           import Task, Note

# import other dependencies
from datetime                           import date
from django.db                          import IntegrityError


# class based APIView for register route
class RegisterAPIView(views.APIView):
    # specifies the serializer class to use for the view.
    serializer_class = RegistrationSerializer

    # a method that returns a dictionary of context information to be passed to the serializer.
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
    
    # a method that returns an instance of the serializer class with the appropriate context.
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    # method that handles HTTP POST requests to the view.
    def post(self, request):
        try:
            # parses the data from request body
            data = JSONParser().parse(request)
            # creates a new instance of the serializer with the parsed data
            serializer = RegistrationSerializer(data=data)

            # checks if the serializer is valid, passing 'raise_exception=True' will allow the serializer to raise an exception when needed
            if serializer.is_valid(raise_exception=True):
                # saves the data and store it to 'user' variable
                user = serializer.save()

                # get the token associated with the created user
                auth_token = Token.objects.get(user=user).key

                # dict to store the message and fetched auth_token
                data = {
                    'message': 'Successfully registered a new user!',
                    'token': auth_token
                }

                # return the 'data' dict with 201 status code
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                # returns an error with 400 status code
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            # returns a JsonResponse if there is an issue with JSON decoding
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
        except IntegrityError:
            # returns an error message when the username is already existing in the database with 400 status code
            return Response({
                'message': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
      
# ViewSet for Task which inherits mixins for list, retrieve, update, create and delete
class TaskViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        viewsets.GenericViewSet
    ):

    # allow only authenticated users to access the endpoints.
    permission_classes = (IsAuthenticated,)

    # specifies TaskSerializer as the serializer class
    serializer_class = TaskSerializer

    # The get_queryset() method is overridden to return all orders for the authenticated user.
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user = user)

    # The create() method is also overridden to handle the creation of new task
    def create(self, request, *args, **kwargs):
        try:
            # parses the data from request body
            data = JSONParser().parse(request)
            # creates a new instance of the serializer with the parsed data
            serializer = TaskSerializer(data=data)

            # checks if the serializer is valid, passing 'raise_exception=True' will allow the serializer to raise an exception when needed
            if serializer.is_valid(raise_exception=True):
                # override the 'user' validated data with the current authenticated user
                serializer.validated_data['user'] = request.user
                # save the data
                serializer.save()

                # dict to store the message and serialized data
                result = {
                    'message': 'Successfully added a new task',
                    'details': serializer.data
                }

                # return the 'result' dict with 201 status code
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                # returns an error with 400 status code
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            # returns a JsonResponse if there is an issue with JSON decoding
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
        
    # The update() method is also overridden to handle the update of a single or more field of task
    def update(self, request, *args, **kwargs):
        try:
            # set partial to True
            partial = kwargs.pop('partial', True)
            # retrieve the task object to be updated
            instance = self.get_object()
            # parse the data from request body
            data = JSONParser().parse(request)
            # serialize the object with the new data that was sent in the request
            serializer = self.get_serializer(instance, data=data, partial=partial)

            # checks if the serializer is valid, passing 'raise_exception=True' will allow the serializer to raise an exception when needed
            if serializer.is_valid(raise_exception=True):
                # invoke 'update' method of serializer and pass the instance and serializer.validated_data as arguments
                serializer.update(instance, serializer.validated_data)

                # dict to store the message and serialized data
                result = {
                    'message': 'Task successfully updated',
                    'details': serializer.data
                }

                # return the 'result' dict with 201 status code
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                # returns an error with 400 status code
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            # returns a JsonResponse if there is an issue with JSON decoding
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
        
    # The destroy() method is also overridden to handle the deleting of a task
    def destroy(self, request, *args, **kwargs):
        try:
            # retrieve the task object to be deleted
            instance = self.get_object()
            # delete the instance from the database
            self.perform_destroy(instance)

            # dict to store the message
            result = {
                "message": "Task successfully deleted"
            }

            # return the 'result' dict with 200 status code
            return Response(result, status=status.HTTP_200_OK)
        except JSONDecodeError:
            # returns a JsonResponse if there is an issue with JSON decoding
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)

# function based APIview for archive and activate task
@api_view(['PATCH'])
# allow only authenticated users to access the endpoint
@permission_classes([IsAuthenticated])
def archive_or_activate_task(request, pk):
    try:
        # get the task object using its pk
        task = Task.objects.get(id=pk)

        # checks if the HTTP method is PATCH
        if request.method == 'PATCH':
            # reverse the status of a task from False to True and vice versa
            task.is_active = not task.is_active
            # modify the message string whether the task is active or not
            message = 'Task activated successfully' if task.is_active else 'Task archived successfully'

            # save the task
            task.save()
            # serialize the data
            serializer = TaskSerializer(task)

            # dict to store the message and serialized data
            result = {
                "message": message,
                "details": serializer.data
            }

            # return the 'result' dict with 200 status code
            return Response(result, status=status.HTTP_200_OK)
    
    except Task.DoesNotExist:
        # returns an error if the task does not exist with 404 status code
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    

class NoteViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
    ):

    permission_classes = (IsAuthenticated,)

    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            serializer = NoteSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.validated_data['user'] = request.user
                serializer.save()

                result = {
                    'message': 'Successfully added a new note',
                    'details': serializer.data
                }

                return Response(result, status=status.HTTP_200_OK)
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
                serializer.update(instance, serializer.validated_data)

                result = {
                    'message': 'Note successfully updated',
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
                'message': 'Note Successfully deleted'
            }

            return Response(result, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
