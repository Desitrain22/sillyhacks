from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Room, User, Dong, Dongable, Location
import random
import string


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


def check_user(request):
    if "user_id" in request.GET:
        user_id = request.GET["user_id"]
        if User.objects.filter(user_id=user_id).exists():
            return JsonResponse({"exists": True})
        return JsonResponse({"exists": False})
    else:
        return HttpResponseBadRequest("Please provide a user_id parameter")


def get_actively_dongable(request):
    if "room_id" in request.GET:
        room_id = request.GET["room_id"]
        room_users = User.objects.filter(room_id=room_id)
        users = Dongable.objects.filter(user__in=room_users)
        dongable = []
        for user in users:
            dongable.append({"user_id": user.user_id, "can_dong": user.can_dong})
        return JsonResponse({"dongable": dongable})
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


def set_dongable(request):
    if "user_id" in request.GET and "can_dong" in request.GET:
        user_id = request.GET["user_id"]
        user = User.objects.get(user_id=user_id)
        # if the user is already dongable, set can_dong to False
        dongable = Dongable.objects.get(user=user)
        dongable.can_dong = True if request.GET["can_dong"] == "1" else False
        dongable.save()
        return JsonResponse({"can_dong": dongable.can_dong})
    else:
        return HttpResponseBadRequest("Please provide a user_id and can_dong parameter")


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
