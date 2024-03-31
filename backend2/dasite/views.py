from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Room, User
import random
import string


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def room(request):
    if 'name' in request.GET:
        name = request.GET['name']
        
        code = generate_code()
        #check if there's a room with the same room_id as code
        while Room.objects.filter(room_id=code).exists():
            code = generate_code()
        room = Room(room_id=code, room_name=name)
        room.save()
        #return a json response 200 with the room_id and room name
        return JsonResponse({"room_id": code, "room_name": name})
    else:
        return HttpResponseBadRequest("Please provide a name parameter")
    
def check_user(request):
    if 'user_id' in request.GET:
        user_id = request.GET['user_id']
        if User.objects.filter(user_id=user_id).exists():
            return JsonResponse({"exists": True})
        return JsonResponse({"exists": False})
    else:
        return HttpResponseBadRequest("Please provide a user_id parameter")

def generate_code():
    code = ''.join(random.choices(string.ascii_uppercase, k=6))
    return code