from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Room, User, Dong, Location, TacoEntryEvent
import random
import string

from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from datetime import datetime, timedelta


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def room(request):
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
        room_id = request.GET["room_id"]
        if Room.objects.filter(room_id=room_id).exists():
            return JsonResponse({"exists": True})
        return JsonResponse({"exists": False})
    else:
        return HttpResponseBadRequest("Please provide a room_id parameter")


def check_user(request):
    if "user_id" in request.GET:
        user_id = request.GET["user_id"]
        if User.objects.filter(user_id=user_id).exists():
            return JsonResponse({"exists": True})
        else:
            if "create" in request.GET:  # create user is username is available
                if "room_id" in request.GET and check_room(request)["exists"]:
                    room_id = request.GET["room_id"]
                    user = User(
                        user_id=user_id, room_id=Room.objects.get(room_id=room_id)
                    )
                    user.save()
                    return JsonResponse(
                        {
                            "exists": True,
                            "user_id": user.user_id,
                            "room_id": user.room_id.room_id,
                        }
                    )
                else:
                    return JsonResponse({"exists": False, "error": "valid room_id required"})
            return JsonResponse({"exists": False})
    else:
        return HttpResponseBadRequest("Please provide a user_id parameter")


def get_actively_dongable(request):
    if "room_id" in request.GET:
        room_id = request.GET["room_id"]
        room = Room.objects.get(room_id=room_id)
        room_users = User.objects.filter(room_id=room)
        entries = [TacoEntryEvent.get_last_user_entry(None, users) for users in room_users]
        result = [
            {
                "user_id": entry.user_id,
                "can_dong": entry.status,
                "location": entry.location.address,
                "timestamp": entry.time,
            }
            for entry in entries
        ]
        return JsonResponse({"dongable": result})
    else:
        return HttpResponseBadRequest("Please provide a room_id parameter")


def get_unloadable(request):
    if "user_id" in request.GET:
        user_id = request.GET["user_id"]
        user = User.objects.get(user_id=user_id)
        dongable = Dong.get_total_unloadable_dongs(None, user)
        return JsonResponse({"dongs_unloadable": dongable})
    else:
        return HttpResponseBadRequest("Please provide a room_id parameter")


def get_loaded_dongs(request):
    if "room_id" in request.GET:
        room = Room.objects.get(room_id=request.GET["room_id"])
        users = User.objects.filter(room_id=room)
        donger = User.objects.get(user_id=request.GET["user_id"])
        result = {}
        for user in users:
            if user != donger:
                dongs = Dong.get_available_dongs(None, donger, user)
                result[user.user_id] = dongs
        return JsonResponse(result)


def get_leaderboard(request):
    if "room_id" in request.GET:
        room_id = request.GET["room_id"]
        users = User.objects.filter(room_id=room_id)
        leaderboard = []
        for user in users:
            leaderboard.append(
                {
                    "user_id": user.user_id,
                    "dong_count": Dong.get_dong_count_for_user(None, user),
                }
            )
        return JsonResponse({"leaderboard": leaderboard})
    else:
        return HttpResponseBadRequest("Please provide a room_id parameter")


def get_dong_history(request):
    if "user_id" in request.GET:
        user_id = request.GET["user_id"]
        user = User.objects.get(user_id=user_id)
        return JsonResponse({"dongs": Dong.get_dong_history(None, user)})
    else:
        return HttpResponseBadRequest("Please provide a user_id parameter")


def dong_by_api(request):
    if "donger" in request.GET and "dongee" in request.GET:
        donger = User.objects.get(user_id=request.GET["donger"])
        dongee = User.objects.get(user_id=request.GET["dongee"])
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
            TacoEntryEvent.get_last_user_entry(None, dongee).status == 1
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


def check_if_at_bell(request):
    lat = float(request.GET["lat"])
    long = float(request.GET["long"])
    locations = Location.objects.all()
    for location in locations:
        if (
            abs(location.latitude - lat) < 0.0002
            and abs(location.longitude - long) < 0.0002
        ):  # within 75 feet of the center of tacobell
            return JsonResponse(
                {
                    "at_bell": True,
                    "location_id": str(location.id),
                    "location_address": str(location.address),
                }
            )
    return JsonResponse({"at_bell": False})


def generate_code():
    code = "".join(random.choices(string.ascii_uppercase, k=6))
    return code
