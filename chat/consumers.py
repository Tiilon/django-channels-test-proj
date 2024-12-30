import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Connection
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["connection_id"]
        self.room_group_name = f"chat_{self.room_name}"
        
        if not self.channel_layer:
            raise ValueError("Channel layer is not configured")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        if not self.channel_layer:
            raise ValueError("Channel layer is not configured")
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data_source = text_data_json.get("source")
        
        if data_source == "chat.message":
            await self.chat_message(text_data_json)
    
    # Receive message from room group
    async def chat_message(self, data):
        message = data["message"]
        
        # Save message to database
        connection = await database_sync_to_async(Connection.objects.get)(id=self.room_name)
        user = self.scope["user"]
        await database_sync_to_async(Message.objects.create)(connection=connection, author=user, content=message)

        # Response data
        data = {
            "message": message,
            "author": user.id,
            "author_name": user.username,
        }
        
        if not self.channel_layer:
            raise ValueError("Channel layer is not configured")
        
        # Send message to room group
        await self.send_group(self.room_group_name, 'chat.message', data)
        
    #--------------------------------------------
	#   Catch/all broadcast to client helpers
	#--------------------------------------------
    async def send_group(self, group, source, data):
        if not self.channel_layer:
            raise ValueError("Channel layer is not configured")
        
        response = {
            "type": "broadcast_group",
            "source": source,
            "data": data,
        }
        await self.channel_layer.group_send(group, response)
        
    async def broadcast_group(self, event):
        '''
		event:
			- type: 'broadcast_group'
			- source: where it originated from
			- data: whatever you want to send as a dict
		'''
		# Send only the source and data to the client
        await self.send(text_data=json.dumps({
            "source": event["source"],
            "data": event["data"],
        }))