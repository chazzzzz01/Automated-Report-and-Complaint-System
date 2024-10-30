# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Complaint
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# @receiver(post_save, sender=Complaint)
# def notify_legal_office(sender, instance, created, **kwargs):
#     if created and instance.office == 'Legal Office':
#         channel_layer = get_channel_layer()
#         total_complaints = Complaint.objects.filter(office='Legal Office').count()
#         total_reports = 0  # You can add logic to count reports if needed

#         async_to_sync(channel_layer.group_send)(
#             'legal_office_notifications',
#             {
#                 'type': 'notify_legal_office',
#                 'message': f'New complaint received: {instance.description}',
#                 'total_complaints': total_complaints,
#                 'total_reports': total_reports
#             }
#         )



from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Informant
from django.contrib.auth.models import User

@receiver(post_save, sender=Informant)
def create_or_update_user(sender, instance, created, **kwargs):
    # Create or update the corresponding User instance
    user, created = User.objects.get_or_create(username=instance.username)
    user.email = instance.email
    user.first_name = instance.first_name
    user.last_name = instance.last_name
    user.is_active = instance.is_active
    user.is_staff = instance.is_staff

    if created:  # Only set the password for new users
        user.set_password(instance.password)  # Hash the password properly
    
    user.save()
