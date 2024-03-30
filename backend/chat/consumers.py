# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from channels.consumer import SyncConsumer

class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept",
        })

    def websocket_receive(self, event):
        message= json.loads(json.loads(event['text'])['message'])
        print(message)
        if message["type"] == "dong":
            if message["status"] == "claimed":
                pass
                #Use up a dong
                #send message to channel, and affected user will get dong notification if name matches
                print('herebtw')
                self.send({
                    "type": "websocket.send",
                    "text": '{"type" : "dong", "status" : "claimed", "donger" : "' + message["donger"] + '", "dongee" : "' + message["dongee"] + '"}',
                })
            else:
                pass
                #Enter new dong
            print(message["donger"])
            print(message["dongee"])
            print(message["status"])
        elif message["type"] == "room":
            # User entering/leaving room
            if message["status"] == "joined":
                pass
                #Add user to room
                self.send({
                    "type": "websocket.send",
                    "text": '{"type" : "room", "status" : "joined", "user" : "' + message["user"] + '"}',})

            else:
                pass
                #Remove user from room
        elif message["type"] == "tacobell":
            if message["status"] == "enter":
                #Make entry that user is in tacobell

                #send notif to users that a dong is available to claim
                self.send({
                    "type": "websocket.send",
                    "text": '{"type" : "tacobell", "status" : "enter", "user" : "' + message["user"] + '"}',})

            else:
                #make entry that user is no longer in the taco bell
        elif message["type"] == "query":
            # User is trying to update leaderboard. Query the "dongs" table and take the standings for the users with matching group ID
            pass
        
        

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
