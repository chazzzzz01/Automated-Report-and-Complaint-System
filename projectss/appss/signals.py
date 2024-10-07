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
