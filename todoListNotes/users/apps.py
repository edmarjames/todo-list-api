from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # The ready() method is called when the Django app is loaded, and is used to perform any necessary initialization or setup for the app.
    def ready(self):
        # By importing the signals module in the ready() method, it ensures that the signals are registered and ready to be used when the app is loaded.
        import users.signals
