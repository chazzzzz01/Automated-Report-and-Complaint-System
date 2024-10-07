import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Complaint

class LegalOfficeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the Legal Office to a notification group
        await self.channel_layer.group_add(
            'legal_office_notifications',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the Legal Office from the notification group
        await self.channel_layer.group_discard(
            'legal_office_notifications',
            self.channel_name
        )

    # Receive a message from the group and send it to WebSocket
    async def notify_legal_office(self, event):
        message = event['message']
        total_complaints = event['total_complaints']
        total_reports = event['total_reports']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'total_complaints': total_complaints,
            'total_reports': total_reports
        }))
