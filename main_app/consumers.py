# main_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import CallRoom
from asgiref.sync import sync_to_async

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'videocall_{self.room_name}'
        
        # Add participant when connecting
        await self.add_participant(self.room_name)
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove participant when disconnecting
        await self.remove_participant(self.room_name)
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'offer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer',
                    'offer': data['offer'],
                    'sender': self.channel_name
                }
            )
        elif message_type == 'answer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer',
                    'answer': data['answer'],
                    'sender': self.channel_name
                }
            )
        elif message_type == 'candidate':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_candidate',
                    'candidate': data['candidate'],
                    'sender': self.channel_name
                }
            )

    async def webrtc_offer(self, event):
        offer = event['offer']
        sender = event['sender']

        if self.channel_name != sender:
            await self.send(text_data=json.dumps({
                'type': 'offer',
                'offer': offer
            }))

    async def webrtc_answer(self, event):
        answer = event['answer']
        sender = event['sender']

        if self.channel_name != sender:
            await self.send(text_data=json.dumps({
                'type': 'answer',
                'answer': answer
            }))

    async def webrtc_candidate(self, event):
        candidate = event['candidate']
        sender = event['sender']

        if self.channel_name != sender:
            await self.send(text_data=json.dumps({
                'type': 'candidate',
                'candidate': candidate
            }))

    @sync_to_async
    def add_participant(self, room_name):
        """Increase participants count when a user joins the room."""
        room = CallRoom.objects.get(name=room_name)
        room.add_participant()

    @sync_to_async
    def remove_participant(self, room_name):
        """Decrease participants count when a user leaves the room."""
        room = CallRoom.objects.get(name=room_name)
        room.remove_participant()


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class VideoCallConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Get room name from URL parameters
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'videocall_{self.room_name}'

#         # Join the room group for signaling
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         # Accept the WebSocket connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group when the WebSocket disconnects
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         # Parse the incoming WebSocket message
#         data = json.loads(text_data)
#         message_type = data.get('type')

#         # Handle WebRTC offer
#         if message_type == 'offer':
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'webrtc_offer',
#                     'offer': data['offer'],
#                     'sender': self.channel_name
#                 }
#             )

#         # Handle WebRTC answer
#         elif message_type == 'answer':
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'webrtc_answer',
#                     'answer': data['answer'],
#                     'sender': self.channel_name
#                 }
#             )

#         # Handle ICE candidate
#         elif message_type == 'candidate':
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'webrtc_candidate',
#                     'candidate': data['candidate'],
#                     'sender': self.channel_name
#                 }
#             )

#     # WebRTC offer broadcasted to other peers
#     async def webrtc_offer(self, event):
#         offer = event['offer']
#         sender = event['sender']

#         # Send the offer to all peers in the room, except the sender
#         if self.channel_name != sender:
#             await self.send(text_data=json.dumps({
#                 'type': 'offer',
#                 'offer': offer
#             }))

#     # WebRTC answer broadcasted to other peers
#     async def webrtc_answer(self, event):
#         answer = event['answer']
#         sender = event['sender']

#         # Send the answer to all peers in the room, except the sender
#         if self.channel_name != sender:
#             await self.send(text_data=json.dumps({
#                 'type': 'answer',
#                 'answer': answer
#             }))

#     # ICE candidate broadcasted to other peers
#     async def webrtc_candidate(self, event):
#         candidate = event['candidate']
#         sender = event['sender']

#         # Send the ICE candidate to all peers in the room, except the sender
#         if self.channel_name != sender:
#             await self.send(text_data=json.dumps({
#                 'type': 'candidate',
#                 'candidate': candidate
#             }))
