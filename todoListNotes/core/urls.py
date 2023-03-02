# import path
from django.urls                        import path

# import dependencies from rest_framework
from rest_framework.authtoken.views     import obtain_auth_token
from rest_framework                     import routers

# import all views
from . views                            import (RegisterAPIView, TaskViewSet, archive_or_activate_task, NoteViewSet)

# A new instance of the DefaultRouter is created using router = routers.DefaultRouter(). This is a convenience class that automatically generates the URL patterns for the API views registered with it.
router = routers.DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'note', NoteViewSet, basename='note')

# The urlpatterns list is then defined using the router's generated URL patterns
urlpatterns = router.urls

# append additional URL patterns to the urlpatterns
urlpatterns += [
    path('users/login', obtain_auth_token, name='login'),
    path('users/register', RegisterAPIView.as_view(), name='register'),
    path('tasks/archive/<uuid:pk>', archive_or_activate_task, name='archive'),
    path('tasks/activate/<uuid:pk>', archive_or_activate_task, name='archive')
]