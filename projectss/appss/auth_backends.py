# from django.contrib.auth.backends import ModelBackend
# from .models import Informant

# class InformantBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             informant = Informant.objects.get(username=username)
#             if informant.check_password(password):
#                 return informant
#         except Informant.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Informant.objects.get(pk=user_id)
#         except Informant.DoesNotExist:
#             return None
