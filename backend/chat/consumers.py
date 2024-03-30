# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer
import pandas as pd

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
                print('herebtw')
                self.log_dong(message["donger"], message["dongee"], message["room_id"], 1)
                self.send({
                    "type": "websocket.send",
                    "text": '{"type" : "dong", "status" : "claimed", "donger" : "' + message["donger"] + '", "dongee" : "' + message["dongee"] + '"}',
                })
            else:
                pass
                self.log_dong(message["donger"], message["dongee"], message["room_id"], 0)
            print(message["donger"])
            print(message["dongee"])
            print(message["status"])
        elif message["type"] == "room":
            # User entering/leaving room
            if message["status"] == "joined":
                self.add_user(message["user"], message["room_id"])
                # self.send({
                #     "type": "websocket.send",
                #     "text": '{"type" : "room", "status" : "joined", "user" : "' + message["user"] + '"}',})
            else:
                pass
                #Remove user from room
        elif message["type"] == "tacobell":
            if message["status"] == "enter":
                self.log_taco_entry(message["user"], message["room_id"], pd.Timestamp.now(), "enter")
                #Make entry that user is in tacobell
                

                #send notif to users that a dong is available to claim
                self.send({
                    "type": "websocket.send",
                    "text": '{"type" : "tacobell", "status" : "enter", "user" : "' + message["user"] + '"}',})

            else:
                #make entry that user is no longer in the taco bell
                self.log_taco_entry(message["user"], message["room_id"], pd.Timestamp.now(), "exit")

        elif message["type"] == "query":
            # User is trying to update leaderboard. Query the "dongs" table and take the standings for the users with matching group ID
            board = self.get_leaderboard(message["room_id"])
            response = ""
            for user in board.index:
                response += '{"user" : "' + user + '", "stat" : "' + board[user] + '"},'
            self.send({
                    "type": "websocket.send",
                    "text": response})

    
    def add_user(self, username, room_id):
        df = pd.read_csv("data/users.csv")
        df.loc[len(df.index)] = [username, room_id]
        df.to_csv("data/users.csv")

    def get_users(self, room_id):
        df = pd.read_csv("data/users.csv")
        return df["room_id" == room_id]

    def get_leaderboard(self, room_id):
        df = pd.read_csv("data/dongs.csv")
        df = df["room_id" == room_id]
        result = df.groupby('donger')['stat'].sum()
        return result
    
    def get_available_dongs(self, room_id):
        df = pd.read_csv("data/tacobell_entry.csv")
        df = df["room_id" == room_id]
        df = df.groupby('username').last()
        return df[df["status"] == "enter"]
    
    def log_taco_entry(self, username, room_id, timestamp, status):
        df = pd.read_csv("data/tacobell_entry.csv")
        df.loc[timestamp] = [username, room_id, status]
        df.to_csv("data/tacobell_entry.csv")

    def log_dong(self, donger, dongee, room_id, status):
        df = pd.read_csv("data/dongs.csv")
        df.loc[len(df.index)] = [donger, dongee, room_id, status]
        df.to_csv("data/dongs.csv", index=False)
        

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
