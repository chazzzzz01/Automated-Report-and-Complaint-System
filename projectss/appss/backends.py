from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from appss.models import Informant

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Check if the user exists in the default User model
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        
        # If not found in User model, check Informant model
        try:
            informant = Informant.objects.get(email=username)
            if informant.check_password(password):
                return informant
        except Informant.DoesNotExist:
            pass
        
        return None

    def get_user(self, user_id):
        # This method retrieves a user or informant by ID
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            try:
                return Informant.objects.get(pk=user_id)
            except Informant.DoesNotExist:
                return None
