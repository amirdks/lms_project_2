import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     pass
from chat_module.models import Chat, Message


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = await self.get_chat()
        self.chat_room_id = f"chat_{self.chat_id}"

        if self.chat:
            await self.channel_layer.group_add(
                self.chat_room_id,
                self.channel_name
            )

            await self.send({
                'type': 'websocket.accept'
            })
        else:
            await self.send({
                'type': 'websocket.close'
            })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room_id,
            self.channel_name
        )
        raise StopConsumer()

    async def websocket_receive(self, event):
        data = json.loads(event.get('text', None))
        message_type = data.get('message_type')
        bytes_data = event.get('bytes', None)

        if message_type == 'message':
            text = data.get('text', None)
            if not text.isspace() and text != '':
                await self.create_message(text)
                await self.channel_layer.group_send(
                    self.chat_room_id,
                    {
                        'type': 'chat_message',
                        'message': json.dumps({'type': "msg", 'sender': self.user.username, 'text': text}),
                        'sender_channel_name': self.channel_name
                    }
                )
            # elif message_type == 'seen_messages':
            #     print('seened')

    async def chat_message(self, event):
        message = event['message']

        if self.channel_name != event['sender_channel_name']:
            await self.send({
                'type': 'websocket.send',
                'text': message
            })

    # async def chat_activity(self, event):
    #     message = event['message']
    #
    #     await self.send({
    #         'type': 'websocket.send',
    #         'text': message
    #     })

    @database_sync_to_async
    def get_chat(self):
        try:
            chat = Chat.objects.get(unique_code=self.chat_id)
            return chat
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, text):
        Message.objects.create(chat_id=self.chat.id, author_id=self.user.id, text=text)
