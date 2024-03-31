import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from dasite.models import User, Room, Dong, Location, TacoEntrance
import hashlib
import uuid


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = json.loads(text_data_json["message"]) 
        print(message)
        
        if message['type'] == 'user':
            #user has entered
            if message["room"] == "create":
                identifier = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:16]
                room = Room(identifier, message["room_name"])
                room.save()
                user = User(user_id = message["user_id"], room_id = room)
                user.save()
            else:
                room = Room.objects.get(room_id = message["room_id"])
                user = User(user_id = message["user_id"], room_id = room)
                user.save()
        elif message['type'] == 'dong':
            donger = User.objects.get(user_id = message["donger"], room_id = Room.objects.get(room_id = message["room_id"]))
            dongee = User.objects.get(user_id = message["dongee"], room_id = Room.objects.get(room_id = message["room_id"]))
            location = Location.objects.get(id = message["location_id"])
            dong = Dong(donger = donger, dongee = dongee, dong_type = message["dong_type"], location = location)
            dong.save()
            if message["dong_type"] == 1: #send dong to donger
                #send dong to dongee
                pass
        elif message['type'] == "TacoEntrance":
            user = User.objects.get(user_id = message["user_id"], room_id = Room.objects.get(room_id = message["room_id"]))
            location = Location.objects.get(id = message["location_id"])
            taco_entrance = TacoEntrance(user = user, location = location, status = message["status"])
            taco_entrance.save()
            if message["status"] == 1: #entering a bell
                #send push to everyone that there's a dong to be claimed
                pass                                 
        
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))