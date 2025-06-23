import json
from channels.generic.websocket import AsyncWebsocketConsumer

'''
Класс для получения сообщений из WS, переписан в данный момент 
не готов, заняться после того как разберусь с подключением к WS 
сделанно'''
class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'post_group',  # Group name
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'post_group',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.send(text_data=json.dumps({
            'title': data.get('title'),
            'content': data.get('content'),
            'id': data.get('id'),
            'author_id': data.get('author_id')
        }))

    async def post_created(self, event):
        post = event['post']

        await self.send(text_data=json.dumps(post))

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.group_name = f'comment_group_{self.post_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.send(text_data=json.dumps({
            'comment': data.get('comment'),
            'comment_id': data.get('comment_id'),
            'post_id': data.get('post_id'),
            'comment_author_id': data.get('comment_author_id')
        }))

    async def comment_created(self, event):
        comment = event['comment']

        await self.send(text_data=json.dumps(comment))