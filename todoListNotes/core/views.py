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
from rest_framework.authtoken.views     import ObtainAuthToken

# import mixins from rest_framework
from rest_framework.mixins              import (ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin)

# import needed serializers
from . serializers                      import RegistrationSerializer, TaskSerializer, NoteSerializer, UserSerializer

# import needed model/s
from django.contrib.auth.models         import User
from . models                           import Task, Note


# import other dependencies
from datetime                           import date
from django.db                          import IntegrityError


# custom login view to include the 'is_superuser' field of a user
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # get the username and password from the request body
        serializer = self.serializer_class(data=request.data, context={'request': request})

        # check if serializer is valid
        if serializer.is_valid(raise_exception=True):
            # store the validated user to the 'user' variable
            user = serializer.validated_data['user']
            # using get_or_create to get the token of the user or create a new one if there is not existing token
            token, created = Token.objects.get_or_create(user=user)

            # dict to store the token, is_superuser and new_token_created
            result = {
                'token': token.key,
                'is_superuser': user.is_superuser,
                'new_token_created': created
            }

            # return the result dict with 200 status code
            return Response(result, status=status.HTTP_200_OK)


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

    # The get_queryset() method is overridden to return all task for the authenticated user.
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
        
    # The update() method is also overridden to handle the update of a single/multiple field of task
    def update(self, request, *args, **kwargs):
        try:
            # set partial to True since this is a PATCH method
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
# allow only authenticated users to access the endpoint
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def archive_task(request, pk):
    try:
        # get the task object using its pk
        task = Task.objects.get(id=pk)

        # checks if the HTTP method is PATCH
        if request.method == 'PATCH':
            # reverse the status of a task from True to False
            if task.is_active == True:
                task.is_active = False
                message = 'Task archived successfully'

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
            
            # if task is already archived
            elif task.is_active == False:
                # return an error message with 400 status code
                return Response({'error': 'Task is already archived'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # returns an error if HTTP method is not PATCH with 405 status code
            return Response({'error', 'Incorrect HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    except Task.DoesNotExist:
        # returns an error if the task does not exist with 404 status code
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    

# function based APIview for archive and activate task
# allow only authenticated users to access the endpoint
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def activate_task(request, pk):
    try:
        # get the task object using its pk
        task = Task.objects.get(id=pk)

        # checks if the HTTP method is PATCH
        if request.method == 'PATCH':
            # reverse the status of a task from False to True
            if task.is_active == False:
                task.is_active = True
                message = 'Task activated successfully'

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
            
            # if task is already activated
            elif task.is_active == True:
                # return an error message with 400 status code
                return Response({'error': 'Task is already activated'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # returns an error if HTTP method is not PATCH with 405 status code
            return Response({'error', 'Incorrect HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    except Task.DoesNotExist:
        # returns an error if the task does not exist with 404 status code
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    

# ViewSet for Note which inherits mixins for list, retrieve, update, create and delete
class NoteViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
    ):

    # allow only authenticated users to access the endpoints.
    permission_classes = (IsAuthenticated,)

    # specifies NoteSerializer as the serializer class
    serializer_class = NoteSerializer

    # The get_queryset() method is overridden to return all notes for the authenticated user.
    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)
    
    # The create() method is also overridden to handle the creation of new note
    def create(self, request, *args, **kwargs):
        try:
            # parses the data from request body
            data = JSONParser().parse(request)
            # creates a new instance of the serializer with the parsed data
            serializer = NoteSerializer(data=data)

            # checks if the serializer is valid, passing 'raise_exception=True' will allow the serializer to raise an exception when needed
            if serializer.is_valid(raise_exception=True):
                # override the 'user' validated data with the current authenticated user
                serializer.validated_data['user'] = request.user
                # save the data
                serializer.save()

                # dict to store the message and serialized data
                result = {
                    'message': 'Successfully added a new note',
                    'details': serializer.data
                }

                # return the 'result' dict with 201 status code
                return Response(result, status=status.HTTP_200_OK)
            else:
                # returns an error with 400 status code
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            # returns a JsonResponse if there is an issue with JSON decoding
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)

    # The update() method is also overridden to handle the update of a single/multiple field of note
    def update(self, request, *args, **kwargs):
        try:
            # set partial to True since this is a PATCH method
            partial = kwargs.pop('partial', True)
            # retrieve the note object to be updated
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
                    'message': 'Note successfully updated',
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
    
    # The destroy() method is also overridden to handle the deleting of a note
    def destroy(self, request, *args, **kwargs):
        try:
            # retrieve the note object to be deleted
            instance = self.get_object()
            # delete the instance from the database
            self.perform_destroy(instance)

            # dict to store the message
            result = {
                'message': 'Note Successfully deleted'
            }

            # return the 'result' dict with 200 status code
            return Response(result, status=status.HTTP_200_OK)
        except JSONDecodeError:
            # returns a JsonResponse if there is an issue with JSON decoding
            return JsonResponse({
                'result': 'error',
                'message': 'JSON decoding error'
            }, status=400)
        

# function based APIview for getting all task of all users
# allow only authenticated users to access the endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_tasks(request):
    if request.method == 'GET':
        # checks if the authenticated user is a superuser
        if request.user.is_superuser:
            # get all task
            all_tasks = Task.objects.all()
            # serialize it
            serializer = TaskSerializer(all_tasks, many=True)
            # return the serialized data with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # if not a superuser, provide an error with 403 status code
            return Response({'forbidden': 'You are not allowed to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # returns an error if HTTP method is not GET with 405 status code
        return Response({'error', 'Incorrect HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# function based APIview for getting all note of all users
# allow only authenticated users to access the endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_notes(request):
    if request.method == 'GET':
        # checks if the authenticated user is a superuser
        if request.user.is_superuser:
            # get all note
            all_notes = Note.objects.all()
            # serialize it
            serializer = NoteSerializer(all_notes, many=True)
            # return the serialized data with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # if not a superuser, provide an error with 403 status code
            return Response({'forbidden': 'You are not allowed to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # returns an error if HTTP method is not GET with 405 status code
        return Response({'error', 'Incorrect HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# function based APIview for getting all users
# allow only authenticated users to access the endpoint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    if request.method == 'GET':
        # checks if the authenticated user is a superuser
        if request.user.is_superuser:
            # get all note
            all_user = User.objects.all()
            # serialize it
            serializer = UserSerializer(all_user, many=True)
            # return the serialized data with 200 status code
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # if not a superuser, provide an error with 403 status code
            return Response({'forbidden': 'You are not allowed to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # returns an error if HTTP method is not GET with 405 status code
        return Response({'error', 'Incorrect HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# function based APIview for setting user as admin
# allow only authenticated users to access the endpoint
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def set_as_admin(request, pk):
    if request.method == 'PATCH':
        # checks if the authenticated user is a superuser
        if request.user.is_superuser:
            try:
                # get the user with the specific pk
                user = User.objects.get(id=pk)

                # if user is not None and not a superuser
                if user and user.is_superuser == False:
                    # set it as superuser/admin
                    user.is_superuser = True
                    # save the updated user
                    user.save()
                    # serialize it
                    serializer = UserSerializer(user)
                    # dict to store the message and serialized data
                    result = {
                        'message': f'Successfully set {user.username} as admin',
                        'details': serializer.data
                    }
                    # return the 'result' dict with 200 status code
                    return Response(result, status=status.HTTP_200_OK)
                
                # if user is not None and already a superuser
                elif user and user.is_superuser == True:
                    # provide an error message with 400 status code
                    return Response({'error': 'User is already a superuser'}, status=status.HTTP_400_BAD_REQUEST)
                    
            except User.DoesNotExist:
                # provide an error message if user does not exists with 404 status code
                return Response({'error': 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # if not a superuser, provide an error with 403 status code
            return Response({'forbidden': 'You are not allowed to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # returns an error if HTTP method is not PATCH with 405 status code
        return Response({'error', 'Incorrect HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# function based APIview for setting user as normal user
# allow only authenticated users to access the endpoint
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def set_as_normal_user(request, pk):
    if request.method == 'PATCH':
        # checks if the authenticated user is a superuser
        if request.user.is_superuser:
            try:
                # get the user with the specific pk
                user = User.objects.get(id=pk)

                # if user is not None and a superuser
                if user and user.is_superuser == True:
                    # revert it as normal user
                    user.is_superuser = False
                    # save the updated user
                    user.save()
                    # serialize it
                    serializer = UserSerializer(user)
                    # dict to store the message and serialized data
                    result = {
                        'message': f'Successfully revert {user.username} as normal user',
                        'details': serializer.data
                    }
                    # return the 'result' dict with 200 status code
                    return Response(result, status=status.HTTP_200_OK)
                
                # if user is not None and already a normal user
                elif user and user.is_superuser == False:
                    # provide an error message with 400 status code
                    return Response({'error': 'User is already a normal user'}, status=status.HTTP_400_BAD_REQUEST)
                
            except User.DoesNotExist:
                # provide an error message if user does not exists with 404 status code
                return Response({'error': 'User does not exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # if not a superuser, provide an error with 403 status code
            return Response({'forbidden': 'You are not allowed to access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # returns an error if HTTP method is not PATCH with 405 status code
        return Response({'error', 'Incorrect HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
            

