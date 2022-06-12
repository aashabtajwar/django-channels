"""
- Consumsers is the Channel's version of Django views
- except they do more than respond to requests from client
- they can also iniate a connection to the client all while keeping an open connection
"""
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer (WebsocketConsumer):

    def connect(self):
        # on initial connection, a group name is set
        # normally, this name is set dynamically from the url
        # or whatever room the user joins

        self.room_group_name = 'test'

        # add 
        async_to_sync(self.channel_layer.group_add)(
            # group room name
            self.room_group_name,
            # creates automically for each user
            self.channel_name       
        )

        self.accept()


        
        # self.send(text_data = json.dumps(
        #     {
        #         'type': 'connection_established',
        #         'message' : 'You are now connected',
        #     }
        # ))

    # listen for messages
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)

        # broadcast message to all users in the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {   
                # specify function that will handle the event
                'type': 'chat_message',
                # the message
                'message': message      
            }
        )




        # self.send(text_data = json.dumps(
        #     {
        #         'type':'chat',
        #         'message': message
        #     }
        # ))
    def chat_message(self, event):
        message = event['message']
        self.send(text_data = json.dumps(
            {
                'type' : 'chat',
                'message': message
            }
        ))
