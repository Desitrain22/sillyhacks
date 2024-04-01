from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Room, User, Dong, Location, TacoEntryEvent, UserDevice
import random
import string
# from pyfcm import FCMNotification
# import os

# API_KEY = os.getenv("FCM_API_KEY")

# def add_users_to_room_topic(room_id: str, registration_ids: list[str]):
#     topic = room_id
#     push_service = FCMNotification(API_KEY)
#     result = push_service.subscribe_registration_ids_to_topic(registration_ids=registration_ids, topic_name=topic)
#     return result

# def send_notification_to_topic(topic_name, title, message):
#     push_service = FCMNotification(API_KEY)
    
#     result = push_service.notify_topic_subscribers(
#         topic_name=topic_name,
#         message_title=title,
#         message_body=message
#     )
    
#     return result

# def notify_dong_available(room_id: str, event: TacoEntryEvent):
#     topic = room_id
#     title = "Dong Available"
#     victim = event.user.user_id
#     location = event.location.address
#     message = f"{victim} just entered The 'Bell at {location}!"
#     return send_notification_to_topic(topic, title, message)

# def notify_dong_sent(room_id: str, donger: User, dongee: User, location: Location):
#     topic = room_id
#     title = "Dong Sent"
#     message = f"{donger.user_id} just sent a dong to {dongee.user_id} at {location.address}!"
#     return send_notification_to_topic(topic, title, message)

from firebase_admin.messaging import Message, Notification
from fcm_django.models import UserDevice

def send_dong_available_to_room(entry_event: TacoEntryEvent):
    topic = entry_event.user.room.room_id
    message = f'{entry_event.user.user_id} just entered The "Bell at {entry_event.location.address}!'
    
    UserDevice.send_topic_message(
        Message(notification=Notification(title="Dong Available!", body=message)), topic
    )
    
    return "dong availability notification sent to {topic}"
    
def send_dong_to_user(dong: Dong):
    device = UserDevice.objects.get(user=dong.dongee)
    device.send_message(Message(notification=Notification(title="Dong Sent!", body=f'{dong.donger.user_id} just sent a dong to you at {dong.location.address}!')))
    return "dong sent to {dong.dongee.user_id}!"

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def create_room(request):
    if "name" in request.GET:
        name = request.GET["name"]
        code = generate_code()
        # check if there's a room with the same room_id as code
        while Room.objects.filter(room_id=code).exists():
            code = generate_code()
        room = Room(room_id=code, room_name=name)
        room.save()
        # return a json response 200 with the room_id and room name
        return JsonResponse({"room_id": code, "room_name": name})
    else:
        return HttpResponseBadRequest("Please provide a name parameter")


def check_room(request):
    if "room_id" in request.GET:
        exists = Room.objects.filter(room_id=request.GET["room_id"]).exists()
        return JsonResponse(
            {
                "room_exists": exists,
                "room_name": (
                    None
                    if not exists  # avoid calling Room.objects.get if the room doesn't exist
                    else Room.objects.get(room_id=request.GET["room_id"]).room_name
                ),
            }
        )
    return HttpResponseBadRequest("Please provide a room_id parameter")


def create_user(request):
    if "user_id" in request.GET and ("room_id" in request.GET):
        if Room.objects.filter(
            room_id=request.GET["room_id"]
        ).exists():  # check if room_id is valid
            room = Room.objects.get(room_id=request.GET["room_id"])
            if User.objects.filter(
                user_id=request.GET["user_id"], room=room
            ).exists():  # make sure the username isn't taken in this room
                return HttpResponseBadRequest("Username already exists in this room")
            user = User(user_id=request.GET["user_id"], room=room)
            user.save()
            return JsonResponse({"user_id": user.user_id, "room_id": user.room.room_id})
    else:
        return HttpResponseBadRequest("Please provide a room_id and user_id parameter")


def get_users_status_for_room(request):
    if (
        "room_id" in request.GET
        and Room.objects.filter(room_id=request.GET["room_id"]).exists()
    ):
        room_id = request.GET["room_id"]
        room = Room.objects.get(room_id=room_id)

        room_users = User.objects.filter(room=room)
        entries = [
            TacoEntryEvent.get_last_user_entry(None, users) for users in room_users
        ]
        result = [
            {
                "user_id": entry.user.user_id,
                "can_dong": entry.status,
                "location": entry.location.address,
                "timestamp": entry.time,
            }
            for entry in entries
            if entry
        ]
        return JsonResponse({"dongable": result})
    else:
        return HttpResponseBadRequest("Please provide a room_id parameter")


def get_total_unloadable(request):
    if (
        "user_id" in request.GET
        and Room.objects.filter(room_id=request.GET["room_id"]).exists()
    ):
        user_id = request.GET["user_id"]
        user = User.objects.get(
            user_id=user_id, room=Room.objects.get(room_id=request.GET["room_id"])
        )
        dongable = Dong.get_total_unloadable_dongs(None, user)
        return JsonResponse({"dongs_unloadable": dongable})
    else:
        return HttpResponseBadRequest("Please provide a room_id parameter")


def get_loaded_dongs(request):
    if (
        "user_id" in request.GET
        and Room.objects.filter(room_id=request.GET["room_id"]).exists()
    ):
        donger = User.objects.get(
            user_id=request.GET["user_id"],
            room=Room.objects.get(room_id=request.GET["room_id"]),
        )
        room = Room.objects.get(room_id=request.GET["room_id"])
        users = User.objects.filter(room=room)

        result = {}
        for user in users:
            if user != donger:
                dongs = Dong.get_available_dongs(None, donger, user)
                result[user.user_id] = dongs
        return JsonResponse(result)


def get_leaderboard(request):
    if "room_id" in request.GET:
        room_id = request.GET["room_id"]
        leaderboard = Dong.get_dong_counts_for_room(
            None, room=Room.objects.get(room_id=room_id)
        )
        leaderboard = {
            list(entry.keys())[0]: list(entry.values())[0] for entry in leaderboard
        }
        users = list(
            User.objects.filter(room=Room.objects.get(room_id=room_id)).values(
                "user_id"
            )
        )
        for user in users:
            if user["user_id"] not in leaderboard:
                leaderboard[user["user_id"]] = 0

        leaderboard = [
            {key: value}
            for key, value in {
                user_id: score
                for user_id, score in sorted(
                    leaderboard.items(), key=lambda item: item[1], reverse=True
                )
            }.items()
        ]
        return JsonResponse({"leaderboard": leaderboard})
    else:
        return HttpResponseBadRequest("Please provide a room_id parameter")


def get_dong_history(request):
    if "user_id" in request.GET and "room_id" in request.GET:
        user_id = request.GET["user_id"]
        user = User.objects.get(
            user_id=user_id, room=Room.objects.get(room_id=request.GET["room_id"])
        )
        return JsonResponse({"dongs": Dong.get_dong_history(None, user)})
    else:
        return HttpResponseBadRequest("Please provide a user_id parameter")


def taco_entry_event(request):
    if all(
        key in request.GET for key in ["user_id", "room_id", "location_id", "status"]
    ):
        user = User.objects.get(
            user_id=request.GET["user_id"],
            room=Room.objects.get(room_id=request.GET["room_id"]),
        )
        location = Location.objects.get(id=request.GET["location_id"])
        status = request.GET["status"]
        room = Room.objects.get(room_id=request.GET["room_id"])
        event = TacoEntryEvent(user=user, room=room, location=location, status=status)
        event.save()
        return JsonResponse(
            {
                "user_id": user.user_id,
                "room_id": room.room_id,
                "location_id": location.id,
                "status": status,
            }
        )
    return HttpResponseBadRequest("Invalid parameters")


def check_if_at_bell(request):
    user = User.objects.get(
        user_id=request.GET["user_id"],
        room=Room.objects.get(room_id=request.GET["room_id"]),
    )
    lat = float(request.GET["lat"])
    long = float(request.GET["long"])
    locations = Location.objects.all()
    for location in locations:
        if (
            abs(location.latitude - lat) < 0.0002
            and abs(location.longitude - long) < 0.0002
        ):  # within 75 feet of the center of tacobell
            if (
                TacoEntryEvent.get_last_user_entry(None, user)
                is None  # If no entrances logged yet
                or TacoEntryEvent.get_last_user_entry(None, user).status
                == 0  # If the last event was a leave
            ):
                event = TacoEntryEvent(
                    user=user,
                    room=user.room,
                    location=location,
                    status=1,
                )
                event.save()
                print("user has entered the bell")
            else:
                print("user still at the bell")
            return JsonResponse(
                {
                    "at_bell": True,
                    "location_id": str(location.id),
                    "location_address": str(location.address),
                }
            )
    if (
        TacoEntryEvent.get_last_user_entry(None, user)
        != None  # If there are any entries
    ) and TacoEntryEvent.get_last_user_entry(
        None, user
    ).status == 1:  # last event was an entrance
        print("user has left the bell")
        event = TacoEntryEvent(
            user=user,
            room=user.room,
            location=location,
            status=0,
        )
        event.save()
    return JsonResponse({"at_bell": False})


def dong_by_api(request):
    if ["donger", "dongee", "room_id", "dong_type"] in request.GET:
        donger = User.objects.get(
            user_id=request.GET["donger"],
            room=Room.objects.get(room_id=request.GET["room_id"]),
        )
        dongee = User.objects.get(
            user_id=request.GET["dongee"],
            room=Room.objects.get(room_id=request.GET["room_id"]),
        )
        dong_type = 1 if request.GET["dong_type"] == "1" else -1
        location = Location.objects.get(id=request.GET["location_id"])
        if (dong_type == -1) and (
            Dong.get_available_dongs(None, donger, dongee) > 0
        ):  # If the user is trying to issue a dong, check if they even can.
            print("dong available, sending dong")
            dong = Dong(
                donger=donger, dongee=dongee, dong_type=dong_type, location=location
            )
            dong.save()
            return JsonResponse(
                {
                    "donger": donger.user_id,
                    "dongee": dongee.user_id,
                    "dong_type": dong_type,
                    "dong_type": dong.dong_type,
                    "location": location.address,
                }
            )
        elif (
            TacoEntryEvent.get_last_user_entry(None, dongee) is not None
            and TacoEntryEvent.get_last_user_entry(None, dongee).status == 1
        ) and dong_type == 1:
            print("user is dongable, issuing dong credit")
            dong = Dong(
                donger=donger,
                dongee=dongee,
                dong_type=dong_type,
                location=location,
            )
            dong.save()
            return JsonResponse(
                {
                    "donger": donger.user_id,
                    "dongee": dongee.user_id,
                    "dong_type": dong_type,
                    "dong_type": dong.dong_type,
                    "location": location.address,
                }
            )
        else:
            print("dong not available")
            return HttpResponseBadRequest("Invalid Dong")


def generate_code():
    code = "".join(random.choices(string.ascii_uppercase, k=6))
    return code
