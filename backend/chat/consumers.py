import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import DatabaseSyncToAsync
from dasite.models import User, Room, Dong, Location, TacoEntryEvent, Dongable


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.display_name = await DatabaseSyncToAsync(self.query_room_name)()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def query_room_name(self):
        return Room.objects.get(room_id=self.room_name).room_name

    def query_room(self):
        return Room.objects.get(room_id=self.room_name)

    def create_user(self, user_id):
        room = self.query_room()
        user = User(user_id=user_id, room_id=room)
        user.save()
        dongable = Dongable(user=user, can_dong=False)
        return user

    def get_user(self, user_id):
        return User.objects.get(
            user_id=user_id,
            room_id=Room.objects.get(room_id=self.room_name),
        )

    def get_location(self, location_id):
        return Location.objects.get(id=location_id)

    def log_entrance(self, location_id, user_id, status):
        location = self.get_location(location_id)
        user = self.get_user(user_id)
        room = self.query_room()
        taco_entrance = TacoEntryEvent(
            user=user, room=room, location=location, status=status
        )
        taco_entrance.save()
        d = Dongable(user=user, can_dong=status)
        d.save()

    def issue_dong(self, donger, dongee, dong_type, location_id):
        donger = self.get_user(donger)
        dongee = self.get_user(dongee)
        location = self.get_location(location_id)
        if (dong_type == -1) and (
            Dong.get_available_dongs(None, donger, dongee) > 0
        ):  # If the user is trying to issue a dong, check if they even can.
            print("dong available, sending dong")
            dong = Dong(
                donger=donger, dongee=dongee, dong_type=dong_type, location=location
            )
            dong.save()
            return dong
        elif (
            Dongable.objects.filter(user=dongee, can_dong=True).exists()
            and dong_type == 1
        ):
            print("user is dongable, issuing dong credit")
            dong = Dong(
                donger=donger,
                dongee=dongee,
                dong_type=dong_type,
                location=location,
            )
            dong.save()
            return dong
        else:
            print("dong not available")
            return None

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = json.loads(text_data_json["message"])

        if message["type"] == "user":
            user = await DatabaseSyncToAsync(self.create_user)(
                user_id=message["user_id"]
            )
            msg = (
                'response: {"type" : "user_joined", "user_id" : "'
                + message["user_id"]
                + '", "room_name" : "'
                + self.display_name
                + '"}'
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": msg,
                },
            )

        elif message["type"] == "dong":
            # Check if message['user_id'] is in Dongable after filtering for true
            dong = await DatabaseSyncToAsync(self.issue_dong)(
                donger=message["donger"],
                dongee=message["dongee"],
                dong_type=message["dong_type"],
                location_id=message["location_id"],
            )

            if message["dong_type"] == -1:  # send dong to donger via push
                response = (
                    '{"type" : "dong_issued", "donger" : "'
                    + message["donger"]
                    + '", "dongee" : "'
                    + message["dongee"]
                    + '"}'
                )
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "chat.message", "message": response}
                )

        elif message["type"] == "taco_entrance":
            taco_entrance = await DatabaseSyncToAsync(self.log_entrance)(
                location_id=message["location_id"],
                user_id=message["user_id"],
                status=message["status"],
            )
            if message["status"] == 1:  # entering a bell
                response = (
                    '{"type" : "dong_available", "dongee" : "'
                    + message["user_id"]
                    + '"}'
                )
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "chat.message", "message": response}
                )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
