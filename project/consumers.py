import json
from channels.generic.websocket import AsyncWebsocketConsumer

class InterfaceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'You are now connected!'
        }))

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        pass


class PersonalAssistantLog(AsyncWebsocketConsumer):
    async def connect(self):
        group_name = 'backend_response'
        await self.channel_layer.group_add(group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        backendChat = json.loads(text_data)
        backendMessage = backendChat['data']
        messageType = backendChat['type']

        if messageType == 'user':
            content = f'<div class="message user-message">{backendMessage}</div>'
            pass
        elif messageType == 'personalAssistant':
            content = f'<div class="message assistant-message">{backendMessage}</div>'
            pass
        self.sendResponse(content)

    async def send_group_message(self, event):
        messageType = event['type-message']
        message = event['data']
        if messageType == 'user':
            content = f'<div class="message user-message">{message}</div>'
            pass
        elif messageType == 'personalAssistant':
            content = f'<div class="message assistant-message">{message}</div>'
            pass
        await self.sendResponse(content)

    async def sendResponse(self,content):
        await self.send(text_data=json.dumps({
            'data':content,
            'type':'response'
        }))
    