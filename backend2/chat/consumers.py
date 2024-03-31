import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from dasite.models import User, Room, Dong, Location, TacoEntrance
import random
import string


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.display_name = Room.objects.get(room_id=self.room_name).room_name

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

        if message["type"] == "user":
            # user has entered
            room = Room.objects.get(room_id=self.room_name)
            user = User(user_id=message["user_id"], room_id=room)
            user.save()
            msg = 'response: {"type" : "user_joined", "user_id" : "' + message["user_id"] + '", "room_name" : "' + self.display_name + '"}'
            print(msg)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": msg,
                },
            )
        elif message["type"] == "dong":
            donger = User.objects.get(
                user_id=message["donger"],
                room_id=Room.objects.get(room_id=self.room_name),
            )
            dongee = User.objects.get(
                user_id=message["dongee"],
                room_id=Room.objects.get(room_id=self.room_name),
            )
            location = Location.objects.get(id=message["location_id"])
            dong = Dong(
                donger=donger,
                dongee=dongee,
                dong_type=message["dong_type"],
                location=location,
            )
            dong.save()
            if message["dong_type"] == 1:  # send dong to donger
                response = (
                    '{"type" : "dong_issued", "donger" : "'
                    + message["donger"]
                    + '", "dongee" : "'
                    + message["dongee"]
                    + '",'
                )
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat.message", "message": response}
                )
                # pass
        elif message["type"] == "taco_entrance":
            user = User.objects.get(
                user_id=message["user_id"],
                room_id=Room.objects.get(room_id=self.room_name),
            )
            location = Location.objects.get(id=message["location_id"])
            taco_entrance = TacoEntrance(
                user=user, location=location, status=message["status"]
            )
            taco_entrance.save()
            if message["status"] == 0:  # entering a bell
                response = (
                    '{"type" : "dong_available", "dongee" : "' + user.user_id + '",'
                )
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "chat.message", "message": response}
                )
        # Send message to room group
        #async_to_sync(self.channel_layer.group_send)(
        #    self.room_group_name, {"type": "chat.message", "message": message}
        #)

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
