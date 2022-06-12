"""
- Consumsers is the Channel's version of Django views
- except they do more than respond to requests from client
- they can also iniate a connection to the client all while keeping an open connection
"""
import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer (WebsocketConsumer):

    def connect(self):
        self.accept()
        
        self.send(text_data = json.dumps(
            {
                'type': 'connection_established',
                'message' : 'You are now connected',
            }
        ))

    # listen for messages
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)