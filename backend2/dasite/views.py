from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Room, User, Dong, Dongable
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


def generate_code():
    code = "".join(random.choices(string.ascii_uppercase, k=6))
    return code
