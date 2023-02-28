# import dependencies for postSave
from django.db.models.signals           import post_save
from django.dispatch                    import receiver

# import needed models
from django.contrib.auth.models         import User

# import Token model from rest_framework
from rest_framework.authtoken.models    import Token

# This code sets up a signal handler using the @receiver decorator. The signal handler is triggered whenever a User instance is saved (either created or updated), and creates a new Token instance for that user
@receiver(post_save, sender=User, weak=False)
def generate_auth_token(sender, instance=None, created=False, **kwargs):

    # If the User instance was just created (i.e., created is True), the function creates a new Token instance for that user by calling Token.objects.create(user=instance). This creates a new token associated with the given user and saves it to the database.
    if created:
        Token.objects.create(user=instance)