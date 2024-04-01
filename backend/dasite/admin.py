from django.contrib import admin

from .models import User, Location, Dong, TacoEntryEvent, Room

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Dong)
admin.site.register(TacoEntryEvent)
admin.site.register(Room)
#admin.site.register(Dongable)
