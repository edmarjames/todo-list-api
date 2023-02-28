from django.urls                        import path

# import obtain_auth_token from rest_framework
from rest_framework.authtoken.views     import obtain_auth_token

# import all views
from . views import RegisterAPIView

urlpatterns = [
    path('users/login', obtain_auth_token, name='login'),
    path('users/register', RegisterAPIView.as_view(), name='register')
]