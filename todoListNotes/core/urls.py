# import path
from django.urls                        import path

# import dependencies from rest_framework
from rest_framework                     import routers

# import all views
from . views                            import (CustomAuthToken, RegisterAPIView, TaskViewSet, archive_task, activate_task, NoteViewSet, get_all_tasks, get_all_notes, get_all_users, set_as_admin, set_as_normal_user)

# A new instance of the DefaultRouter is created using router = routers.DefaultRouter(). This is a convenience class that automatically generates the URL patterns for the API views registered with it.
router = routers.DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'note', NoteViewSet, basename='note')

# The urlpatterns list is then defined using the router's generated URL patterns
urlpatterns = router.urls

# append additional URL patterns to the urlpatterns
urlpatterns += [
    path('users/login', CustomAuthToken.as_view(), name='login'),
    path('users/register', RegisterAPIView.as_view(), name='register'),
    path('tasks/archive/<uuid:pk>', archive_task, name='archive'),
    path('tasks/activate/<uuid:pk>', activate_task, name='archive'),
    path('all_tasks', get_all_tasks, name='all_task'),
    path('all_notes', get_all_notes, name='all_notes'),
    path('all_users', get_all_users, name='all_users'),
    path('set_as_admin/<int:pk>', set_as_admin, name='set_as_admin'),
    path('set_as_normal_user/<int:pk>', set_as_normal_user, name='set_as_normal_user')
]