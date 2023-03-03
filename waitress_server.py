import sys
import os
from waitress import serve
# from todoListNotes.wsgi import application
from django.core.wsgi import get_wsgi_application


# Add the directory containing the "todoListNotes" package to the Python path
# sys.path.insert(0, 'todoListNotes\\todoListNotes')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'todoListNotes')))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoListNotes.settings')

# Get the WSGI application
application = get_wsgi_application()

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=8000)